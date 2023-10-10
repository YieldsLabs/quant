use crate::exit_mapper::{map_to_exit, ExitConfig};
use crate::filter_mapper::{map_to_filter, FilterConfig};
use crate::signal_mapper::{map_to_signal, SignalConfig};
use crate::stop_loss_mapper::{map_to_stoploss, StopLossConfig};
use base::register_strategy;

fn create_and_register(
    signal: SignalConfig,
    filter: FilterConfig,
    stoploss: StopLossConfig,
    exit: ExitConfig,
) -> i32 {
    let mapped_signal = map_to_signal(signal);
    let mapped_filter = map_to_filter(filter);
    let mapped_stoploss = map_to_stoploss(stoploss);
    let mapped_exit = map_to_exit(exit);

    register_strategy(mapped_signal, mapped_filter, mapped_stoploss, mapped_exit)
}

#[no_mangle]
pub fn register_cross3ma(
    smoothing: f32,
    short_period: f32,
    medium_period: f32,
    long_period: f32,
    atr_period: f32,
    atr_factor: f32,
) -> i32 {
    create_and_register(
        SignalConfig::Ma3Cross {
            smoothing,
            short_period,
            medium_period,
            long_period,
        },
        FilterConfig::Dumb {
            period: long_period,
        },
        StopLossConfig::Atr {
            period: atr_period,
            multi: atr_factor,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_crosstii(
    major_period: f32,
    minor_period: f32,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: f32,
    period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    create_and_register(
        SignalConfig::TIICross {
            major_period,
            minor_period,
            lower_barrier,
            upper_barrier,
        },
        FilterConfig::Ma { smoothing, period },
        StopLossConfig::Atr {
            period: atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_crossrsin(
    rsi_type: f32,
    rsi_period: f32,
    threshold: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    create_and_register(
        SignalConfig::RsiNeutralityCross {
            rsi_type,
            rsi_period,
            threshold,
        },
        FilterConfig::Dumb { period: rsi_period },
        StopLossConfig::Atr {
            period: atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_rsivma(
    rsi_type: f32,
    rsi_period: f32,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: f32,
    period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    create_and_register(
        SignalConfig::RsiV {
            rsi_type,
            rsi_period,
            lower_barrier,
            upper_barrier,
        },
        FilterConfig::Ma { smoothing, period },
        StopLossConfig::Atr {
            period: atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_rsi2ma(
    rsi_type: f32,
    rsi_period: f32,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: f32,
    short_period: f32,
    long_period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    create_and_register(
        SignalConfig::Rsi2Ma {
            rsi_type,
            rsi_period,
            lower_barrier,
            upper_barrier,
            smoothing,
            short_period,
            long_period,
        },
        FilterConfig::Dumb {
            period: long_period,
        },
        StopLossConfig::Atr {
            period: atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_ground(
    smoothing: f32,
    smoothing_period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    create_and_register(
        SignalConfig::Testground {
            smoothing,
            smoothing_period,
        },
        FilterConfig::Dumb {
            period: smoothing_period,
        },
        StopLossConfig::Atr {
            period: atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_candlet(
    candle: f32,
    smoothing: f32,
    period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    create_and_register(
        SignalConfig::Trendcandle { candle },
        FilterConfig::Ma { smoothing, period },
        StopLossConfig::Atr {
            period: atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_snatr(
    atr_period: f32,
    atr_smoothing_period: f32,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: f32,
    period: f32,
    stop_loss_atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    create_and_register(
        SignalConfig::SnAtr {
            atr_period,
            atr_smoothing_period,
            lower_barrier,
            upper_barrier,
        },
        FilterConfig::Ma { smoothing, period },
        StopLossConfig::Atr {
            period: stop_loss_atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}
