TA_LIB_PATH := ta_lib/Cargo.toml

.PHONY: test check build

test:
	cargo test --manifest-path=$(TA_LIB_PATH)

check:
	cargo fmt --all --check --manifest-path=$(TA_LIB_PATH)
	cargo clippy --all-features --all-targets --workspace --manifest-path=$(TA_LIB_PATH)

build:
	RUSTFLAGS="-C target-feature=+multivalue" cargo build --release --manifest-path=$(TA_LIB_PATH) --package trend_follow --target wasm32-wasi