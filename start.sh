#!/bin/sh

ROOTDIR="$(pwd)/PypiReCom/"
ENVDIR="$ROOTDIR/env"
APPDIR="$ROOTDIR/Demo101"

LOGDIR="$ROOTDIR/logs/"
BACKENDLOG="$LOGDIR/backend.log"
FRONTENDLOG="$LOGDIR/frontend.log"

#start

echo "start script started! \n"
echo "checking if repo Exists."

#Get the kernel name using the 'uname' command
kernel_name=$(uname -s)
hardware_name=$(uname -m)

# Check if the system is macOS or linux
if [ "$kernel_name" == "Darwin" ] || [ "$kernel_name" == "Linux" ]; then

    #Installing OS level dependencies
    if [ "$kernel_name" == "Darwin" ]; then
        echo "System detected : macOS $hardware_name"

        #installing git
        if ! command -v git > /dev/null 2>&1; then
            brew install git
        fi


    elif [ "$kernel_name" == "Linux" ]; then
        echo "System detected : Linux $hardware_name"
        
        #installing git
        if ! command -v git > /dev/null 2>&1; then
            sudo apt install git-all
        fi

    fi
    sleep 0.8

    if [ -d "PypiReCom" ]
        then
            echo "repo exists"

        else
            echo "repo not found."
            echo "downloading PyPiReCom repository \n"
            #cloning git
            git clone https://github.com/Animesh2210/PypiReCom.git
            echo "\nrepo downloaded at $(pwd)/PyPiReCom"
    fi
        
    #changing branch
    echo "\nchecking out to Demo101 branch"

    cd $ROOTDIR
    git fetch --all
    git checkout -b Demo101 origin/Demo101

    #Check if virtualenv/venv exists
    #create virtualenv as env on location $ENV
    if command -v venv > /dev/null 2>&1 ; then
        venv env $ENV
        echo "created virtual environment at $ENV "

    elif command -v virtualenv > /dev/null 2>&1 ; then
        virtualenv env $ENV
        echo "created virtual environment at $ENV "

    else
        pip3 install virtualenv
        virtualenv env $ENV
        echo "created virtual environment at $ENV "
    fi

    #activating environment
    source $ENVDIR/bin/activate
    echo "\ncreated and activated virtual environment."

    #installing requirements file
    pip install -r $APPDIR/requirements.txt

    #creating logs folder
    if ! [ -d "$ROOTDIR/logs" ]; then
        mkdir $LOGDIR
    fi

    echo "\n\n"
    echo "
    ██████╗░██╗░░░██╗██████╗░██╗██████╗░███████╗░█████╗░░█████╗░███╗░░░███╗
    ██╔══██╗╚██╗░██╔╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗██╔══██╗████╗░████║
    ██████╔╝░╚████╔╝░██████╔╝██║██████╔╝█████╗░░██║░░╚═╝██║░░██║██╔████╔██║
    ██╔═══╝░░░╚██╔╝░░██╔═══╝░██║██╔══██╗██╔══╝░░██║░░██╗██║░░██║██║╚██╔╝██║
    ██║░░░░░░░░██║░░░██║░░░░░██║██║░░██║███████╗╚█████╔╝╚█████╔╝██║░╚═╝░██║
    ╚═╝░░░░░░░░╚═╝░░░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚══════╝░╚════╝░░╚════╝░╚═╝░░░░░╚═╝ 🄳 🄴 🄼 🄾"
    echo "\n\n"

    url="http://localhost:8501"
    echo "Demo is running on ${url}. Press ctrl+c/control+c to quit"

    #activating backend server and frontend server
    cd $APPDIR
    uvicorn main:app --reload >> $BACKENDLOG 2>&1 &
    pid1=$!

    streamlit run $APPDIR/Frontend/1_Search\ Package.py >> $FRONTENDLOG 2>&1 &
    pid2=$!

    # Closing app
    cleanup() {
        echo "Performing cleanup..."
        echo "\nShutting down the backend server"
        lsof -ti :8000 | xargs kill

        echo "Shutting down the frontend server"
        lsof -ti :8501 | xargs kill

        echo "\nClosing the app..."
        exit 1
    }
    #detect control+c
    trap cleanup SIGINT

    #waiting for both servers to finish loading
    wait $pid1
    wait $pid2
# If neither macOS nor Linux, assume it's a different operating system
else
    echo "System Detected : Unknown\n"
    echo "exiting.."
    sleep 0.5

    #Exiting
    exit 1
fi
