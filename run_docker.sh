

sudo docker run --gpus all --rm -it -e DISPLAY=$DISPLAY -v $(pwd):/myapp -v /tmp/.X11-unix:/tmp/.X11-unix:rw --device="/dev/video0:/dev/video0" --device="/dev/snd:/dev/snd" --device /dev/dri nikitakesha13/walmart_vision:latest
