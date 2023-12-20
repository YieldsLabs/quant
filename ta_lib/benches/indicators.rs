use core::prelude::*;
use criterion::{criterion_group, criterion_main, Criterion};
use momentum::apo;

fn momentum(c: &mut Criterion) {
    let mut group = c.benchmark_group("momentum");

    group.bench_function("apo", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from([
                    6.6430, 6.8595, 6.8680, 6.8650, 6.8445, 6.8560, 6.8565, 6.8590, 6.8530, 6.8575,
                    6.855, 6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365,
                    6.8310, 6.8355, 6.8360, 6.8345, 6.8285, 6.8395,
                ]);
                let short_period = 10;
                let long_period = 20;
                (source, short_period, long_period)
            },
            |(source, short_period, long_period)| apo(source, *short_period, *long_period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.finish();
}

criterion_group!(indicators, momentum);

criterion_main!(indicators);
