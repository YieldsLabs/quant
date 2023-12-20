use core::prelude::*;
use criterion::{criterion_group, criterion_main, Criterion};
use momentum::{apo, stc};

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

    group.bench_function("stc", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from([
                    6.855, 6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365,
                    6.8310, 6.8355, 6.8360, 6.8345, 6.8285, 6.8395, 7.1135, 7.088, 7.112, 7.1205,
                    7.1195, 7.136, 7.1405, 7.112, 7.1095, 7.1220, 7.1310, 7.1550, 7.1480, 7.1435,
                    7.1405, 7.1440, 7.1495, 7.1515, 7.1415, 7.1445, 7.1525, 7.1440, 7.1370, 7.1305,
                    7.1375, 7.1250, 7.1190, 7.1135, 7.1280, 7.1220, 7.1230, 7.1225, 7.1180, 7.1250,
                    7.1230, 7.1130, 7.1210, 7.13, 7.134, 7.132, 7.116, 7.1235, 7.1645, 7.1565,
                    7.1560,
                ]);
                let fast_period = 23;
                let slow_period = 50;
                let cycle = 10;
                let d_first = 3;
                let d_second = 3;
                (source, fast_period, slow_period, cycle, d_first, d_second)
            },
            |(source, fast_period, slow_period, cycle, d_first, d_second)| {
                stc(
                    source,
                    *fast_period,
                    *slow_period,
                    *cycle,
                    *d_first,
                    *d_second,
                )
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.finish();
}

criterion_group!(indicators, momentum);

criterion_main!(indicators);
