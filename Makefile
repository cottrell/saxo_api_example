# UID := $(shell uuidgen)
UID := makefile_example

run:
	echo CONTEXT_ID is $(UID)
	./example_sub.py create-price-sub $(UID) XAUUSD GBPUSD
	./example_sub.py read-sub $(UID)

cleanup:
	./example_sub.py delete-price-sub $(UID)
