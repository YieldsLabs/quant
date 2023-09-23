TA_LIB_DIR := ta_lib
WASM_DIR := wasm
TA_LIB_PATH := $(TA_LIB_DIR)/Cargo.toml

.PHONY: test check build

test:
	cargo test --manifest-path=$(TA_LIB_PATH)

check:
	cargo clippy --all-features --all-targets --workspace --manifest-path=$(TA_LIB_PATH)
	cargo fmt --all --check --manifest-path=$(TA_LIB_PATH)

build:
	RUSTFLAGS="-C target-feature=+multivalue" cargo build --release --manifest-path=$(TA_LIB_PATH) --package trend_follow --target wasm32-wasi
	mv $(TA_LIB_DIR)/target/wasm32-wasi/release/trend_follow.wasm $(WASM_DIR)/trend_follow.wasm

run:
	pipenv run python3 quant.py