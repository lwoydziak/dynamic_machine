#!/bin/bash

PYTHON3=python3
PYTHON2=python

for P in wget ant "${PYTHON3}" python3-pip  "${PYTHON2}" python-pip python-virtualenv cython3 debconf oracle-java8-installer
do
	if ! dpkg-query -s $P | grep ok.installed >/dev/null 2>&1
	then
		echo "package $P not found; installing..."
		if [ "$P" = "oracle-java8-installer" ]; then
    		sudo apt-get install -y software-properties-common
			sudo add-apt-repository ppa:webupd8team/java
			sudo apt-get update --fix-missing
			echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
    	fi
		sudo apt-get install -y $P
		if [ "$P" == "$PYTHON_VERSION" ]; then
			sudo update-alternatives --install /usr/bin/python python /usr/bin/$PYTHON_VERSION 10
		fi			
	fi
done

pip2 freeze > .pipPackageList

for P in clonedigger
do
        python2 find_package.py --package $P .pipPackageList
        case $? in
        1)
                echo "Python package $P not found, installing..."
        		y="sudo pip install $P"
        		$y
                ;;
        2)
                echo "Python package $P needs upgrade, upgrading..."
        		y="sudo pip install --upgrade $P"
        		$y
                ;;
        esac
done

rm -f .pipPackageList

rm -rf .python3-sandbox
virtualenv -p python3 .python3-sandbox
pip3_file=".python3-sandbox/bin/pip3"
if [ ! -e "$pip3_file" ]
then
	ln -s .python3-sandbox/bin/pip*3* .python3-sandbox/bin/pip3
fi

