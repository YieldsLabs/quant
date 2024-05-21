use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct TechAnalysis {
    pub rsifast: Vec<f32>,
    pub rsislow: Vec<f32>,
    pub mafast: Vec<f32>,
    pub maslow: Vec<f32>,
    pub macd: Vec<f32>,
    pub vo: Vec<f32>,
    pub nvol: Vec<f32>,
    pub tr: Vec<f32>,
    pub bbp: Vec<f32>,
    pub k: Vec<f32>,
    pub d: Vec<f32>,
    pub hh: Vec<f32>,
    pub ll: Vec<f32>,
}
