#!/bin/bash
# works for os x el capitan

get_input(){
    input=''
    while [ ! "$input" = 'y' ] && [ ! "$input" = 'n' ]
    do
	read -s -p "Enter {y|n}" -e input
    done
}

postgres_setup(){
    echo "We're now going to do some setup..."

    echo "Do you want postgres to start at login?"
    get_input
  
    if [ "$input" = "y" ]
    then
	ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents
    fi

    echo "Starting postgres..."
    pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start

    echo "Sleeping for a second while postgres starts..."
    sleep 1
    
    echo "Creating postgres user..."
    createuser postgres

    echo "Creating app database..."
    input=''
    while [ -z "$input" ]
    do
	read -s -p "Enter database name: " -e input
    done

    createdb -O postgres "$input"

    echo "Setting up database with flask..."
    echo "Delete migrations folder?"
    get_input

    if [ "$input" = "y" ]
    then
	rm -rf migrations
	python db.py db init
    fi

    python db.py db migrate
    python db.py db upgrade

    echo "Setup finished..."
}

remove_postgres(){
    pg_ctl -D /usr/local/var/postgres stop -s -m fast
    brew uninstall postgres
    rm -rf /usr/local/var/postgres
}

case $1 in
    start)
	which -s psql
	if [ "$?" = "1" ]
	then
	    echo "Postgres is not installed, ./postgres.sh install to install."
	else
	    pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
	fi
	;;
    stop)
	if [ "$?" = "1" ]
	then
	    echo "Postgres is not installed, ./postgres.sh install to install."
	else
	    pg_ctl -D /usr/local/var/postgres stop -s -m fast
	fi
	;;
    status)
	if [ "$?" = "1" ]
	then
	    echo "Postgres is not installed, ./postgres.sh install to install."
	else
	    pg_ctl -D /usr/local/var/postgres status
	fi
	;;
    update)
	python db.py db migrate
	python db.py db upgrade
	;;
    install)
	which -s psql
	if [ "$?" = "0" ]
	then
	    echo "Postgres is already installed."
	else
	    which -s brew
	    res=$?

	    if [ "$res" = "1" ]
	    then
		echo "brew is not installed. Install brew?"
		get_input

		if [ "$input" = "y" ]
		then
		    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

		    brew install postgres
		    postgres_setup
		fi
	    elif [ "$res" = "0" ]
	    then
		brew install postgres
		postgres_setup
	    fi
	fi
	;;
    uninstall)
	which -s psql
	if [ "$?" = "1" ]
	then
	    echo "Postgres is already uninstalled."
	else
	    echo "Are you sure? This will delete all data stored in postgres."
	    get_input

	    if [ "$input" = "y" ]
	    then
		which -s brew
		res=$?

		if [ "$res" = "1" ]
		then
		    echo "brew is not installed. Install brew?"
		    get_input

		    if [ "$input" = "y" ]
		    then
			/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

			remove_postgres
		    fi
		elif [ "$res" = "0" ]
		then
		    remove_postgres
		fi
	    fi
	fi
	;;
    *)
	echo $"Usage: $0 {start|stop|status|update|install|uninstall}"
	exit 1
esac
