import pytorch_lightning as pl
from astrochem_embedding.pipeline.data import MaskedStringDataModule
from astrochem_embedding import get_paths
from astrochem_embedding.models import models
import os

pl.seed_everything(215015)

BATCH_SIZE = 128
NUM_WORKERS = os.cpu_count() - 2
EMBEDDING_DIM = 128
Z_DIM = 32
NUM_LAYERS = 1
LR = 1e-4


def main():
    model = models.VICGAE(EMBEDDING_DIM, Z_DIM, NUM_LAYERS, lr=LR)

    data = MaskedStringDataModule(BATCH_SIZE, NUM_WORKERS)

    logger = pl.loggers.TensorBoardLogger(
        "tb_logs", name="VICAstrochemEmbedder", log_graph=True
    )
    summarizer = pl.callbacks.ModelSummary(max_depth=-1)

    trainer = pl.Trainer(max_epochs=5, callbacks=[summarizer], logger=logger)
    trainer.fit(model, data)

    paths = get_paths()
    trainer.save_checkpoint(paths.get("models").joinpath("VICGAE_new.ckpt"))


if __name__ == "__main__":
    main()
