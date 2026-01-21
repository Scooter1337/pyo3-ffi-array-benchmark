use pyo3::prelude::*;
use std::time::{SystemTime, UNIX_EPOCH};

#[pyfunction]
fn await_timestamps(py: Python, count: usize) -> PyResult<Bound<'_, PyAny>> {
    pyo3_async_runtimes::tokio::future_into_py(py, async move {
        let mut out = Vec::with_capacity(count);
        for _ in 0..count {
            let now = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .map_err(|e| {
                    PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!(
                        "system clock error: {e}"
                    ))
                })?;
            out.push(now.as_nanos() as u64);
        }
        Ok(out)
    })
}

#[pyfunction]
fn timestamps(count: usize) -> PyResult<Vec<u64>> {
    let mut out = Vec::with_capacity(count);
    for _ in 0..count {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map_err(|e| {
                PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!(
                    "system clock error: {e}"
                ))
            })?;
        out.push(now.as_nanos() as u64);
    }
    Ok(out)
}

#[pyfunction]
fn await_timestamps_bytes(py: Python, count: usize) -> PyResult<Bound<'_, PyAny>> {
    pyo3_async_runtimes::tokio::future_into_py(py, async move {
        let mut out = Vec::with_capacity(count * 8);
        for _ in 0..count {
            let now = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .map_err(|e| {
                    PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!(
                        "system clock error: {e}"
                    ))
                })?;
            out.extend_from_slice(&now.as_nanos().to_le_bytes());
        }
        Ok(out)
    })
}

#[pyfunction]
fn timestamps_bytes(count: usize) -> PyResult<Vec<u8>> {
    let mut out = Vec::with_capacity(count * 8);
    for _ in 0..count {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map_err(|e| {
                PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!(
                    "system clock error: {e}"
                ))
            })?;
        out.extend_from_slice(&now.as_nanos().to_le_bytes());
    }
    Ok(out)
}

#[pymodule]
fn pyo3_ffi_array_benchmark(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(await_timestamps, m)?)?;
    m.add_function(wrap_pyfunction!(await_timestamps_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(timestamps, m)?)?;
    m.add_function(wrap_pyfunction!(timestamps_bytes, m)?)?;
    Ok(())
}
