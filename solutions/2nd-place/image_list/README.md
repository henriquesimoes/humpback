# Training and validation data update

In order to test this solution with other dataset configuration, some files had to be updated and new splits had to be created. More specifically, the `test{n}.{valid,train}.txt` files were created using the [create_validation](create_validation.py) script, by passing the test 1 and test 2 train CSV files. The validation proportion used was calculated from the previous validation splits (600 / 25361), created by the solution's author.

To use these files, the [data processing script](../process/data.py) was updated as well.
