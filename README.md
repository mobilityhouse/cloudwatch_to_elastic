AWS Cloudwatch to Elastic
=========================

A lambda function to forward AWS Cloud watch to your private ElasticSearch
cloud.

How do you use this?
--------------------

Copy `config.mk.example` to `config.mk` run edit `config.mk` hit `make publish`.
Hit enter, go get your coffee. In a few minutes your lambda function is all
set.

You can add more pre-processing logging before submitting the message by adding
a module called `custom_filter` with a single function called `run`. If this
module will be found it will be imported and the function will be run before
actually submitting the message to ElasticSearch.
