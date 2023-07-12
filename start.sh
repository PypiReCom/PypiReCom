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

if [ -d "PypiReCom" ]
	then
		echo "repo exists"

	else
		echo "repo not fount."
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

if [[ $? -ne 0 && $(checkout Demo101 origin/Demo101 2>&1) == *"error: pathspec 'origin/Demo101' did not match any file(s) known to git"* ]]; then
	echo "Branch not found, creating new branch."
    git checkout Demo101 origin/Demo101
else
    echo "\ncreating vitual environment"
    # Continue script execution
fi

#creating virtual environment
virtualenv env $ENV

#activating environment
source $ENVDIR/bin/activate
echo "\ncreated and activated vitual environment"

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
