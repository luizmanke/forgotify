FLAGS := 


guard-%:
	@if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set!"; \
		exit 1; \
	fi
	
update: guard-STACK
	pulumi update -s ${STACK} ${FLAGS}

destroy: guard-STACK
	pulumi destroy -s ${STACK} ${FLAGS}

list-stacks:
	pulumi stack ls
