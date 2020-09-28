"""
Sample the csv file at a specific rate (for example pulses at 38Khz).
Transform the sampled data to pulses at the specified rate.
"""
from itertools import groupby
from typing import List
import click
from utils import frequency_to_milliseconds, Signal, Sample, load_file, remove_start_offset, \
    dump_signals_to_file_as_cpp_code, convert_samples_to_milliseconds


def determine_number_of_signals(samples: List[Sample], frequency: int) -> int:
    sampling_time = samples[-1].timestamp - samples[0].timestamp
    return int(sampling_time * frequency)


def get_value_from_sample_at_offset(samples: List[Sample], offset: float, start_from=0):
    for index in range(start_from, len(samples)):
        if samples[index].timestamp > offset:
            return samples[index - 1].value, index
    raise Exception("Offset to big, no data.")


def sample_samples_at_specific_frequency(samples, number_of_signals, frequency) -> List[int]:
    offset_between_signals_in_seconds = frequency_to_milliseconds(frequency)
    values = []
    last_index = 0

    for signal_index in range(number_of_signals):
        signal_offset = offset_between_signals_in_seconds * signal_index
        signal_value, last_index = get_value_from_sample_at_offset(samples, signal_offset, start_from=last_index)
        values.append(signal_value)

    return values


def merge_same_signals_into_one(signals: List[int], frequency: int) -> List[Signal]:
    grouped_signals = []
    for signal_value, signal_group in groupby(signals):
        signal_length = frequency_to_milliseconds(frequency) * len(list(signal_group))
        grouped_signals.append(Signal(length=signal_length, value=signal_value))
    return grouped_signals


@click.command()
@click.argument('sample_file_path', type=click.Path(exists=True))
@click.argument('template_file_path', type=click.Path(exists=True))
@click.argument('output_file_path', type=click.Path(exists=False))
@click.argument('frequency', type=int)
def generate_data_file(sample_file_path: str, template_file_path, output_file_path: str, frequency: int):
    samples = load_file(sample_file_path)
    samples_without_offset = remove_start_offset(samples)
    samples_in_milliseconds = convert_samples_to_milliseconds(samples_without_offset)
    number_of_signals = determine_number_of_signals(samples_in_milliseconds, frequency)
    signals = sample_samples_at_specific_frequency(samples_in_milliseconds, number_of_signals, frequency)
    merged_signals = merge_same_signals_into_one(signals, frequency)
    dump_signals_to_file_as_cpp_code(merged_signals, template_file_path, output_file_path)


if __name__ == '__main__':
    generate_data_file()
