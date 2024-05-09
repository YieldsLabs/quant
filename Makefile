TA_LIB_DIR := ta_lib
WASM_DIR := wasm
TA_LIB_PATH := $(TA_LIB_DIR)/Cargo.toml

.PHONY: test check build

test:
	cargo test --manifest-path=$(TA_LIB_PATH)

bench:
	cargo bench --manifest-path=$(TA_LIB_PATH) --package benches

check:
	cargo clippy --all-features --all-targets --workspace --manifest-path=$(TA_LIB_PATH)
	cargo fmt --all --check --manifest-path=$(TA_LIB_PATH)

build: build-timeseries build-strategy

build-strategy:
	RUSTFLAGS="-C target-feature=+multivalue,+simd128 -C link-arg=-s" cargo build --release --manifest-path=$(TA_LIB_PATH) --package trend_follow --target wasm32-wasi
	cp $(TA_LIB_DIR)/target/wasm32-wasi/release/trend_follow.wasm $(WASM_DIR)/trend_follow.wasm

build-timeseries:
	RUSTFLAGS="-C target-feature=+multivalue,+simd128 -C link-arg=-s" cargo build --release --manifest-path=$(TA_LIB_PATH) --package ffi --target wasm32-wasi
	cp $(TA_LIB_DIR)/target/wasm32-wasi/release/ffi.wasm $(WASM_DIR)/timeseries.wasm

run:
	pipenv run python3 quant.py

format:
	cargo fmt --all --manifest-path=$(TA_LIB_PATH)
	pipenv run black .
	pipenv run ruff . --fix