from typing import List

import click

from utils import Sample, Signal, load_file, remove_start_offset, convert_samples_to_milliseconds, \
    dump_signals_to_file_as_cpp_code


def convert_samples_to_signals(samples: List[Sample]) -> List[Signal]:
    signals = []
    for index in range(len(samples) - 1):
        length = samples[index + 1].timestamp - samples[index].timestamp
        print(length)
        value = samples[index].value
        signals.append(Signal(length=length, value=value))
    signals.append(Signal(length=signals[-1].length, value=samples[-1].value))
    return signals


@click.command()
@click.argument('sample_file_path', type=click.Path(exists=True))
@click.argument('template_file_path', type=click.Path(exists=True))
@click.argument('output_file_path', type=click.Path(exists=False))
@click.argument('frequency', type=int)
def generate_data_file(sample_file_path: str, template_file_path, output_file_path: str, frequency: int):
    samples = load_file(sample_file_path)
    samples_without_offset = remove_start_offset(samples)
    samples_in_milliseconds = convert_samples_to_milliseconds(samples_without_offset)
    signals = convert_samples_to_signals(samples_in_milliseconds)
    dump_signals_to_file_as_cpp_code(signals, template_file_path, output_file_path)


if __name__ == '__main__':
    generate_data_file()
