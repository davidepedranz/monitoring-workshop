#!/bin/sh

backend_1="http://backend-1:5000"
backend_2="http://backend-2:5000"

while true
do

    # calls to a not-existing endpoint
    for _ in $(seq 20); do
        curl -s -X GET "${backend_1}/not-existing-endpoint" > /dev/null
    done

    sleep 5

    # calls to existing endpoints (note that we are doing 2x calls to backend_1)
    for _ in $(seq 10); do
        for backend in $backend_1 $backend_1 $backend_2; do

            # create a Todo
            text="[original] From bot to ${backend} at $(date)"
            id=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"text\": \"${text}\"}" "${backend}/todos/" | jq --raw-output ".id")

            # update the Todo
            text="[edited] From bot to ${backend} at $(date)"
            curl -s -X PATCH -H "Content-Type: application/json" -d "{\"text\": \"${text}\"}" "${backend}/todos/${id}" > /dev/null

            # activate and deactivate the Todo
            curl -s -X POST "${backend}/todos/${id}/activate" > /dev/null
            curl -s -X POST "${backend}/todos/${id}/deactivate" > /dev/null

            # get the single Todo and the list
            curl -s -X GET "${backend}/todos/${id}" > /dev/null
            curl -s -X GET "${backend}/todos/" > /dev/null

            # delete the Todo
            curl -s -X DELETE "${backend}/todos/${id}" > /dev/null
        done

        # create and delete a Todo, possibly bugged
        id=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"text\": \"bug\"}" "${backend-2}/todos/" | jq --raw-output ".id")
        curl -s -X DELETE "${backend}/todos/${id}" > /dev/null
    done

    sleep 10
done
