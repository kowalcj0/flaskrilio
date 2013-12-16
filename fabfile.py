
# tasks:
# http://docs.fabfile.org/en/1.8/tutorial.html
spawn ec2 instance
install dependencies
deploy code
start flaskrilio in background
run behave tests
download junit report
download flaskrilio db
download all the logs (flaskrilio, behave, plain output)
