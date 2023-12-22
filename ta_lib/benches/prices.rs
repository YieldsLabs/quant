use core::prelude::*;
use criterion::{criterion_group, criterion_main, Criterion};
use price::prelude::*;

fn price(c: &mut Criterion) {
    let mut group = c.benchmark_group("price");
    let open: Vec<f32> = vec![
        6.8430, 6.8660, 6.8635, 6.8610, 6.865, 6.8595, 6.8565, 6.852, 6.859, 6.86, 6.8580, 6.8605,
        6.8620, 6.867, 6.859, 6.8670, 6.8640, 6.8575, 6.8485, 6.8350, 7.1195, 7.136, 7.1405, 7.112,
        7.1095, 7.1520, 7.1310, 7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495, 7.1515, 7.1415,
        7.1445, 7.1525, 7.1440, 7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135, 7.1280, 7.1220,
        7.1330, 7.1225, 7.1180, 7.1250,
    ];

    let high: Vec<f32> = vec![
        6.8430, 6.8660, 6.8685, 6.8690, 6.865, 6.8595, 6.8565, 6.862, 6.859, 6.86, 6.8580, 6.8605,
        6.8620, 6.86, 6.859, 6.8670, 6.8640, 6.8575, 6.8485, 6.8450, 7.1195, 7.136, 7.1405, 7.112,
        7.1095, 7.1220, 7.1310, 7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495, 7.1515, 7.1415,
        7.1445, 7.1525, 7.1440, 7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135, 7.1280, 7.1220,
        7.1230, 7.1225, 7.1180, 7.1250,
    ];

    let low: Vec<f32> = vec![
        6.8380, 6.8430, 6.8595, 6.8640, 6.8435, 6.8445, 6.8510, 6.8560, 6.8520, 6.8530, 6.8550,
        6.8550, 6.8565, 6.8475, 6.8480, 6.8535, 6.8565, 6.8455, 6.8445, 6.8365, 7.1195, 7.136,
        7.1405, 7.112, 7.1095, 7.1220, 7.1310, 7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495,
        7.1515, 7.1415, 7.1445, 7.1525, 7.1440, 7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135,
        7.1280, 7.1220, 7.1230, 7.1225, 7.1180, 7.1250,
    ];

    let close: Vec<f32> = vec![
        6.855, 6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365, 6.8310, 6.8355,
        6.8360, 6.8345, 6.8285, 6.8395, 7.1135, 7.088, 7.112, 7.1205, 7.1195, 7.136, 7.1405, 7.112,
        7.1095, 7.1220, 7.1310, 7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495, 7.1515, 7.1415,
        7.1445, 7.1525, 7.1440, 7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135, 7.1280, 7.1220,
        7.1230, 7.1225, 7.1180, 7.1250,
    ];

    group.bench_function("ohlc4", |b| {
        b.iter_batched_ref(
            || {
                let open = Series::from(&open);
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);

                (open, high, low, close)
            },
            |(open, high, low, close)| average_price(open, high, low, close),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("hl2", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);

                (high, low)
            },
            |(high, low)| median_price(high, low),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("hlc3", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);

                (high, low, close)
            },
            |(high, low, close)| typical_price(high, low, close),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("wcl", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);

                (high, low, close)
            },
            |(high, low, close)| wcl(high, low, close),
            criterion::BatchSize::SmallInput,
        )
    });

    group.finish();
}

criterion_group!(prices, price);
criterion_main!(prices);
