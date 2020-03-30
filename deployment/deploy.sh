owd=$PWD
project_dir='/root/OS3-RLL-Python'

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
    echo "deploying..."
    set_env
    git pull --no-edit
    python3 setup.py install
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
    cd $project_dir
    deploy
    start $1
elif [[ $1 == "run_only" ]]; then
    set_env
    start "debug"
else
    echo "unknown param $1"
    echo "usage: $0 <prod|debug|run_only>"
fi

trap clean_up EXIT
