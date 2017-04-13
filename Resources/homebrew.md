# Installing Homebrew

Homebrew is a MacOS package manager that can be utilized to download development and testing tools. 
### To install:
Open terminal  and enter:
```sh
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

If that doesn't work, go to the [Homebrew] (http://brew.sh) website and copy the install command into terminal. 
The installation process can take time so give your machine time to complete the entirety of the download. 

### Using Homebrew: 

>The format of most brew install commands:  brew install nameOfProgramYouWantToInstall

- Warning: Do not enter sudo with the brew command , your machine will yell at you

An example:


```sh
$ brew install PyQt
```

- Homebrew usually links the newly installed program to /usr/local/bin/. 

If there is an issue go to the application directory of the application you installed and try:
```sh
$ cp ./bin/* /usr/local/bin
```
This command just moves the necessary files to /usr/local/bin which enables you to execute your program/application in all directories where there are the necessary program input and script files.

[Homebrew]: <http://brew.sh>


