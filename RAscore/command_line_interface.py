import click
import logging
import os
import pandas as pd

logger = logging.getLogger(__name__)

@click.command()
@click.option(
    '--file_path',
    '-f',
    help='Absolute path to input file containing one SMILES on each line. The column should be labelled "SMILES" or if another header is used, specify it as an option'
)
@click.option(
    '--column_header',
    '-c',
    default="SMILES",
    help='The name given to the singular column in the file which contains the SMILES'
)
@click.option(
    '--output_path', 
    '-o', 
    help='Output file path'
)
@click.option(
    '--model_path',
    '-m',
    help='Absoulte path to the model to use, if .h5 file neural network in tensorflow/keras, if .pkl then XGBoost'
)

def main(
    file_path: str, output_path: str, model_path: str
) -> None:
    if file_path.endswith('.txt'):
        df = pd.read_csv(file_path, names=[column_header])
    elif file_path.endswith('.smi'):
        df = pd.read_csv(file_path, names=[column_header])
    elif file_path.endswith('.tsv'):
        df = pd.read_csv(file_path, sep='\t', names=[column_header])
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path, names=[column_header])
    else:
        ValueError('Unrecognized file type')

    if model_path.endswith('.h5'):
        from RAscore import RAscore_NN #For tensorflow and keras based models
        scorer = RAscore_NN.RAScorerNN(model_path)
    elif model_path.endswith('.pkl'): 
        from RAscore import RAscore_XGB #For XGB based models
        scorer = RAscore_XGB.RAScorerXGB(model_path)
    else:
        ValueError('Unrecognized model type, must end in .h5 for tensorflow/keras models or .pkl for xgboost')

    df['RAscore'] = df[column_header].apply(scorer.predict)

    df.to_csv(output_path, index=False)

if __name__ == '__main__':
    main()