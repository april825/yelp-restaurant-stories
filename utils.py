from time import perf_counter
import functools
import pandas as pd


def timer(f):
    @functools.wraps(f)
    def wrapper_timer(*args, **kwargs):
        time_start = perf_counter()
        value = f(*args, **kwargs)
        time_end = perf_counter()
        time_run = time_end - time_start
        print(f"Finished {f.__name__!r} in {time_run:.3f} secs\n")
        return value

    return wrapper_timer


def print_data_info(df):
    print(f"Memory: {df.memory_usage(deep=True).sum():,.0f} bytes")
    print(f" Shape: {df.shape}\n")


@timer
def load_print_data(path, filename, filetype="csv"):
    if filetype == "csv":
        df = pd.read_csv(
            path + filename + "." + filetype, encoding="utf-8-sig", low_memory=False
        )
    elif filetype == "parquet":
        df = pd.read_parquet(path + filename + "." + filetype, encoding="utf-8-sig")
    elif filetype == "json":
        df = pd.read_json(
            path + filename + "." + filetype, encoding="utf-8", lines=True
        )
    print(f"  File: {filename}")
    print_data_info(df)
    return df


def load_data(path, filename):
    df = load_print_data(path, filename)
    df.columns = [i.strip() for i in df.columns]
    for col in [i for i in df.columns if "date" in i]:
        df[col] = pd.to_datetime(df[col]).dt.date
    df_sample = df.sample(min(len(df), 8))
    return df, df_sample


def save_file(df, path, filename, fmt="csv", condition=None):
    t0 = perf_counter()
    df_out = df if condition is None else df[condition]
    if fmt == "csv":
        df_out.to_csv(path + filename + ".csv", index=False, encoding="utf-8-sig")
    else:
        df_out.to_excel(
            excel_writer=(path + filename + "." + fmt), sheet_name="DATA", index=False
        )
    rt_min, t_now = calc_rt(t0)
    dur = f"{rt_min*60:,.2f} sec" if rt_min < 1 else f"{rt_min:,.2f} min"
    print(
        f'file: "{filename}" took {dur} to save and was last saved on {t_now:%Y/%m/%d %H:%M:%S}'
    )
