if [ $# -ge 2 ]; then
    command="pytest "
    module=""
    cov=""

    for i in $*; do
        module="$module $i"
        cov="$cov --cov=$i/tests/"
    done

    $command$module$cov
elif [ $1 = 'all' ]; then
    # this line will execute all module 
    pytest --cov=customer/tests/ --cov=company/tests/ --cov=department/tests/ --cov=vendor/tests/ --cov=branch/tests/ --cov=contact_person/tests/ --cov=entity/tests/ --cov=product/tests/ --cov=port/tests/  --cov=enquiry_management/tests/ --cov=quote/tests/
else
    # this line will execute the single module as pytest branch --cov=branch/tests
    pytest $1 --cov=$1/tests/   
fi
