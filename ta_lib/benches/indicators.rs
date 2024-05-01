use core::prelude::*;
use criterion::{criterion_group, criterion_main, Criterion};
use momentum::*;
use price::prelude::*;
use trend::*;
use volatility::*;
use volume::*;

fn momentum(c: &mut Criterion) {
    let mut group = c.benchmark_group("momentum");
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

    group.bench_function("ao", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let source = median_price(&high, &low);
                let smooth_type = Smooth::SMA;
                let fast_period = 5;
                let slow_period = 34;

                (source, smooth_type, fast_period, slow_period)
            },
            |(source, smooth_type, fast_period, slow_period)| {
                ao(source, *smooth_type, *fast_period, *slow_period)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("bop", |b| {
        b.iter_batched_ref(
            || {
                let open = Series::from(&open);
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let smooth_type = Smooth::SMA;
                let smoothing_period = 14;
                (open, high, low, close, smooth_type, smoothing_period)
            },
            |(open, high, low, close, smooth_type, smoothing_period)| {
                bop(open, high, low, close, *smooth_type, *smoothing_period)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("cc", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let smooth_type = Smooth::WMA;
                let fast_period = 20;
                let slow_period = 15;
                let smoothing_period = 13;
                (
                    source,
                    smooth_type,
                    fast_period,
                    slow_period,
                    smoothing_period,
                )
            },
            |(source, smooth_type, fast_period, slow_period, smoothing_period)| {
                cc(
                    source,
                    *fast_period,
                    *slow_period,
                    *smooth_type,
                    *smoothing_period,
                )
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("cci", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let hlc3 = typical_price(&high, &low, &close);
                let smooth_type = Smooth::SMA;
                let period = 14;
                let factor = 0.015;
                (hlc3, smooth_type, period, factor)
            },
            |(hlc3, smooth_type, period, factor)| cci(hlc3, *smooth_type, *period, *factor),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("cfo", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 14;
                (source, period)
            },
            |(source, period)| cfo(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("cmo", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 14;
                (source, period)
            },
            |(source, period)| cmo(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("di", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let smooth_type = Smooth::WMA;
                let period = 14;
                (source, smooth_type, period)
            },
            |(source, smooth_type, period)| di(source, *smooth_type, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("dmi", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let smooth_type = Smooth::SMMA;
                let adx_period = 14;
                let di_period = 14;
                let atr = atr(&high, &low, &close, Smooth::SMMA, di_period);
                (high, low, atr, smooth_type, adx_period, di_period)
            },
            |(high, low, atr, smooth_type, adx_period, di_period)| {
                dmi(high, low, atr, *smooth_type, *adx_period, *di_period)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("kst", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let smooth_type = Smooth::SMA;
                let roc_period_first = 10;
                let roc_period_second = 15;
                let roc_period_third = 20;
                let roc_period_fouth = 30;
                let period_first = 10;
                let period_second = 10;
                let period_third = 10;
                let period_fouth = 15;

                (
                    source,
                    smooth_type,
                    roc_period_first,
                    roc_period_second,
                    roc_period_third,
                    roc_period_fouth,
                    period_first,
                    period_second,
                    period_third,
                    period_fouth,
                )
            },
            |(
                source,
                smooth_type,
                roc_period_first,
                roc_period_second,
                roc_period_third,
                roc_period_fouth,
                period_first,
                period_second,
                period_third,
                period_fouth,
            )| {
                kst(
                    source,
                    *smooth_type,
                    *roc_period_first,
                    *roc_period_second,
                    *roc_period_third,
                    *roc_period_fouth,
                    *period_first,
                    *period_second,
                    *period_third,
                    *period_fouth,
                )
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("macd", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let smooth = Smooth::EMA;
                let fast_period = 15;
                let slow_period = 26;
                let signal_period = 9;
                (source, smooth, fast_period, slow_period, signal_period)
            },
            |(source, smooth, fast_period, slow_period, signal_period)| {
                macd(source, *smooth, *fast_period, *slow_period, *signal_period)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("roc", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 9;
                (source, period)
            },
            |(source, period)| roc(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("rsi", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let smooth_type = Smooth::SMMA;
                let period = 14;
                (source, smooth_type, period)
            },
            |(source, smooth_type, period)| rsi(source, *smooth_type, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("stc", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let smooth_type = Smooth::EMA;
                let fast_period = 23;
                let slow_period = 50;
                let cycle = 10;
                let d_first = 3;
                let d_second = 3;
                (
                    source,
                    smooth_type,
                    fast_period,
                    slow_period,
                    cycle,
                    d_first,
                    d_second,
                )
            },
            |(source, smooth_type, fast_period, slow_period, cycle, d_first, d_second)| {
                stc(
                    source,
                    *smooth_type,
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

    group.bench_function("stochosc", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let smooth_type = Smooth::SMA;
                let period = 14;
                let k_period = 5;
                let d_period = 5;
                (high, low, close, smooth_type, period, k_period, d_period)
            },
            |(high, low, close, smooth_type, period, k_period, d_period)| {
                stochosc(
                    high,
                    low,
                    close,
                    *smooth_type,
                    *period,
                    *k_period,
                    *d_period,
                )
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("tii", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let smooth_type = Smooth::SMA;
                let major_period = 30;
                let minor_period = 10;
                (source, smooth_type, major_period, minor_period)
            },
            |(source, smooth_type, major_period, minor_period)| {
                tii(source, *smooth_type, *major_period, *minor_period)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("trix", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let smooth_type = Smooth::EMA;
                let period = 18;
                (source, smooth_type, period)
            },
            |(source, smooth_type, period)| trix(source, *smooth_type, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("tsi", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let smooth_type = Smooth::EMA;
                let slow_period = 25;
                let fast_period = 13;
                (source, smooth_type, slow_period, fast_period)
            },
            |(source, smooth_type, slow_period, fast_period)| {
                tsi(source, *smooth_type, *slow_period, *fast_period)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.finish();
}

fn trend(c: &mut Criterion) {
    let mut group = c.benchmark_group("trend");
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

    let volume: Vec<f32> = vec![
        60.855, 600.858, 60.86, 600.848, 60.8575, 60.864, 600.8565, 60.8455, 600.845, 600.8365,
        60.8310, 60.8355, 600.836, 60.8345, 600.8285, 60.8395, 700.1135, 70.088, 700.112, 70.1205,
        700.1195, 70.136, 70.1405, 70.112, 700.1095, 70.1220, 70.1310, 700.155, 70.1480, 70.1435,
        700.1405, 70.1440, 70.1495, 70.1515, 70.1415, 700.1445, 70.1525, 700.144, 70.1370,
        700.1305, 70.1375, 700.125, 700.119, 70.1135, 70.128, 700.122, 70.123, 700.1225, 70.118,
        70.125,
    ];

    group.bench_function("alma", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;
                let offset = 0.85;
                let sigma = 6.0;

                (source, period, offset, sigma)
            },
            |(source, period, offset, sigma)| alma(source, *period, *offset, *sigma),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("ast", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let atr_period = 14;
                let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);
                let factor = 3.0;

                (close, atr, factor)
            },
            |(close, atr, factor)| ast(close, atr, *factor),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("ce", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let atr_period = 14;
                let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);
                let factor = 3.0;
                let period = 20;

                (close, atr, period, factor)
            },
            |(close, atr, period, factor)| ce(close, atr, *period, *factor),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("chop", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let atr_period = 14;
                let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);
                let period = 20;

                (high, low, atr, period)
            },
            |(high, low, atr, period)| chop(high, low, atr, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("dema", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| dema(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("dpo", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let smooth_type = Smooth::SMA;
                let period = 20;

                (source, smooth_type, period)
            },
            |(source, smooth_type, period)| dpo(source, *smooth_type, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("ema", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| ema(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("frama", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let period = 20;

                (high, low, close, period)
            },
            |(high, low, close, period)| frama(high, low, close, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("gma", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| gma(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("hma", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| hma(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("kama", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| kama(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("kjs", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let period = 20;

                (high, low, period)
            },
            |(high, low, period)| kjs(high, low, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("lsma", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| lsma(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("md", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| md(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("qstick", |b| {
        b.iter_batched_ref(
            || {
                let open = Series::from(&open);
                let close = Series::from(&close);
                let smooth_type = Smooth::EMA;
                let period = 20;

                (open, close, smooth_type, period)
            },
            |(open, close, smooth_type, period)| qstick(open, close, *smooth_type, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("rmsma", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| rmsma(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("sinwma", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| sinwma(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("sma", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| sma(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("smma", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| smma(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("supertrend", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let hl2 = median_price(&high, &low);
                let atr_period = 14;
                let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);
                let factor = 3.0;

                (hl2, close, atr, factor)
            },
            |(hl2, close, atr, factor)| supertrend(hl2, close, atr, *factor),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("t3", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| t3(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("tema", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| tema(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("tma", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| tma(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("vwma", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let volume = Series::from(&volume);
                let period = 20;

                (source, volume, period)
            },
            |(source, volume, period)| vwma(source, volume, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("wma", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| wma(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("zlema", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| zlema(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("zlsma", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 20;

                (source, period)
            },
            |(source, period)| zlsma(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.finish();
}

fn volatility(c: &mut Criterion) {
    let mut group = c.benchmark_group("volatility");

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

    group.bench_function("atr", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let smooth_type = Smooth::SMMA;
                let period = 14;

                (high, low, close, smooth_type, period)
            },
            |(high, low, close, smooth_type, period)| atr(high, low, close, *smooth_type, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("bb", |b| {
        b.iter_batched_ref(
            || {
                let close = Series::from(&close);
                let smooth_type = Smooth::SMA;
                let period = 14;
                let factor = 3.0;

                (close, smooth_type, period, factor)
            },
            |(close, smooth_type, period, factor)| bb(close, *smooth_type, *period, *factor),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("dch", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let period = 14;

                (high, low, period)
            },
            |(high, low, period)| dch(high, low, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("kb", |b| {
        b.iter_batched_ref(
            || {
                let close = Series::from(&close);
                let period = 14;
                let factor = 3.0;

                (close, period, factor)
            },
            |(close, period, factor)| kb(close, *period, *factor),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("kch", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let hlc3 = typical_price(&high, &low, &close);
                let atr_period = 14;
                let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);
                let smooth_type = Smooth::EMA;
                let period = 14;
                let factor = 3.0;

                (hlc3, atr, smooth_type, period, factor)
            },
            |(hlc3, atr, smooth_type, period, factor)| {
                kch(hlc3, atr, *smooth_type, *period, *factor)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("ppb", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let smooth_type = Smooth::SMA;
                let period = 14;
                let factor = 3.0;

                (high, low, close, smooth_type, period, factor)
            },
            |(high, low, close, smooth_type, period, factor)| {
                ppb(high, low, close, *smooth_type, *period, *factor)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("snatr", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let atr_period = 14;
                let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);
                let smooth_type = Smooth::WMA;
                let smoothing_period = 3;

                (atr, atr_period, smooth_type, smoothing_period)
            },
            |(atr, atr_period, smooth_type, smoothing_period)| {
                snatr(atr, *atr_period, *smooth_type, *smoothing_period)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("tr", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);

                (high, low, close)
            },
            |(high, low, close)| tr(high, low, close),
            criterion::BatchSize::SmallInput,
        )
    });

    group.finish();
}

fn volume(c: &mut Criterion) {
    let mut group = c.benchmark_group("volume");

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

    let volume: Vec<f32> = vec![
        60.855, 600.858, 60.86, 600.848, 60.8575, 60.864, 600.8565, 60.8455, 600.845, 600.8365,
        60.8310, 60.8355, 600.836, 60.8345, 600.8285, 60.8395, 700.1135, 70.088, 700.112, 70.1205,
        700.1195, 70.136, 70.1405, 70.112, 700.1095, 70.1220, 70.1310, 700.155, 70.1480, 70.1435,
        700.1405, 70.1440, 70.1495, 70.1515, 70.1415, 700.1445, 70.1525, 700.144, 70.1370,
        700.1305, 70.1375, 700.125, 700.119, 70.1135, 70.128, 700.122, 70.123, 700.1225, 70.118,
        70.125,
    ];

    group.bench_function("cmf", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let volume = Series::from(&volume);
                let period = 14;

                (high, low, close, volume, period)
            },
            |(high, low, close, volume, period)| cmf(high, low, close, volume, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("eom", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let volume = Series::from(&volume);
                let hl2 = median_price(&high, &low);
                let smooth_type = Smooth::SMA;
                let period = 14;
                let divisor = 10000.0;

                (hl2, high, low, volume, smooth_type, period, divisor)
            },
            |(hl2, high, low, volume, smooth_type, period, divisor)| {
                eom(hl2, high, low, volume, *smooth_type, *period, *divisor)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("mfi", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let volume = Series::from(&volume);
                let hlc3 = typical_price(&high, &low, &close);
                let period = 14;

                (hlc3, volume, period)
            },
            |(hlc3, volume, period)| mfi(hlc3, volume, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("obv", |b| {
        b.iter_batched_ref(
            || {
                let close = Series::from(&close);
                let volume = Series::from(&volume);

                (close, volume)
            },
            |(close, volume)| obv(close, volume),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("vo", |b| {
        b.iter_batched_ref(
            || {
                let volume = Series::from(&volume);
                let fast_period = 5;
                let slow_period = 10;
                let smooth_type = Smooth::EMA;

                (volume, smooth_type, fast_period, slow_period)
            },
            |(volume, smooth_type, fast_period, slow_period)| {
                vo(volume, *smooth_type, *fast_period, *slow_period)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("vwap", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let volume = Series::from(&volume);
                let hlc3 = typical_price(&high, &low, &close);

                (hlc3, volume)
            },
            |(hlc3, volume)| vwap(hlc3, volume),
            criterion::BatchSize::SmallInput,
        )
    });

    group.finish();
}

criterion_group!(indicators, momentum, trend, volatility, volume);
criterion_main!(indicators);
