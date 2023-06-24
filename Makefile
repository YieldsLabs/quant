.PHONY: test check

TA_LIB_PATH ?= ta_lib/Cargo.toml

test:
	cargo test --manifest-path=$(TA_LIB_PATH)

check:
	cargo fmt --all --check --manifest-path=$(TA_LIB_PATH)
	cargo clippy --all-features --all-targets --workspace --manifest-path=$(TA_LIB_PATH)