use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct TechAnalysis {
    pub frsi: Vec<f32>,
    pub srsi: Vec<f32>,
    pub fma: Vec<f32>,
    pub sma: Vec<f32>,
    pub froc: Vec<f32>,
    pub sroc: Vec<f32>,
    pub macd: Vec<f32>,
    pub cci: Vec<f32>,
    pub obv: Vec<f32>,
    pub vo: Vec<f32>,
    pub nvol: Vec<f32>,
    pub tr: Vec<f32>,
    pub bbp: Vec<f32>,
    pub k: Vec<f32>,
    pub d: Vec<f32>,
    pub hh: Vec<f32>,
    pub ll: Vec<f32>,
}
