owd=$PWD
project_dir='/root/OS3-RLL-Python'
python_bin=$(which python3.8 || which python3)

function set_env() {
    if [[ -z $RLL_ENV ]]; then
	echo "sourcing /etc/default/os3-rocket-league-ladder"
        set -a
        source /etc/default/os3-rocket-league-ladder
        set +a
        export RLL_ENV='configured'
    fi
}

function deploy() {
    cd $project_dir
    echo "cleaning pyc files..."
    find . -name '*.pyc' -delete
    echo "deploying..."
    set_env
    echo "Discarding local changes"
    git reset --hard HEAD~1
    git pull --no-edit
    python_bin setup.py install
}

function start() {
    echo "staring as $1..."
    if [[ $1 == "prod" ]]; then
        systemctl restart os3-rocket-league-ladder.service
    elif [[ $1 == "debug" ]]; then
	systemctl stop os3-rocket-league-ladder.service
        os3-rocket-league-ladder -v
    else
	systemctl stop os3-rocket-league-ladder.service
    fi
}

function clean_up() {
    echo "cleaning up" 
    cd $owd
}

if [[ $1 == "prod" || $1 == "debug" ]]; then
    deploy
    start $1
elif [[ $1 == "run_only" ]]; then
    set_env
    start "debug"
else
    echo "unknown param $1"
    echo "This deploy script will clean the working dir, pull the latest version from git and deploy it"
    echo "usage: $0 <prod|debug|run_only>"
fi

trap clean_up EXIT
