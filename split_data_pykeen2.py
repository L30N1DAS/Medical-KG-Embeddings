from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
from matplotlib import pyplot as plt
import utils

#from pykeen.datasets.nations import NATIONS_TRAIN_PATH


if __name__ == "__main__":
    import pandas as pd
    import os

    tsv_dir = "tsv_dir"
    output_dir = "transe-input-pykeen"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the TSV file
    for tsv_file in ["pharmacy_output_data.tsv", "patient_output_data.tsv", "imaging_output_data.tsv"]:
        df = pd.read_csv(os.path.join(tsv_dir, tsv_file), sep='\t')
        df = utils.read_all_save_unique(df)
        
        df.to_csv(os.path.join(tsv_dir, tsv_file.replace(".tsv", "_unique.tsv")), sep='\t', index=False)

        # Save the data
        if not os.path.isfile(f'{output_dir}/all_triples.txt'):
            df.to_csv(f'{output_dir}/all_triples.txt', header=False, sep = '\t', index = False)
        else:
            df.to_csv(f'{output_dir}/all_triples.txt', mode='a', sep='\t', header=False, index=False)


        tf = TriplesFactory.from_path(f'{output_dir}/all_triples.txt')

        training, testing, validation = tf.split([.8, .1, .1])

        # result = pipeline(

            # training=training,

            # testing=testing,

            # validation=validation,

            # model='TransE',

            # stopper='early',

            # epochs=100,  # short epochs for testing - you should go

                    # higher, especially with early stopper enabled

        # )

        result = pipeline(
            training=training,
            testing=testing,
            validation=validation,
            model='TransE',
            model_kwargs=dict(embedding_dim=2),
            # random_seed=1,
            # device='cpu',
            stopper='early',
            epochs=100,
        )

        plt.plot(result.losses)
        plt.savefig("plot.png")

        # Save eval metrics in csv ( for link prediction )
        if result.metric_results:
            eval_metrics = result.metric_results.to_dict()
            metrics_df = pd.DataFrame(eval_metrics)
            # metrics_file = os.path.join(output_path, "metrics.csv")
            # metrics_df.to_csv(metrics_file, index=False)
            metrics_file = os.path.join(output_dir, "metrics.csv")
            metrics_df.to_csv(metrics_file, index=False)
            print(f"Evaluation results saved in {metrics_file}")
        else:
            print("No evaluation results available.")

        print(vars(training).keys())
        print(training.metadata)
        #print(training.entity_labeling) #mapped_triples is tensors

        result.save_to_directory('transe-input-pykeen')
