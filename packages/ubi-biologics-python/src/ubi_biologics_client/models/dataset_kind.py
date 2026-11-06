from enum import Enum


class DatasetKind(str, Enum):
    ALIGNMENT = "alignment"
    ANNOTATED_SEQUENCES = "annotated_sequences"
    ASSAY = "assay"
    CHROMATOGRAMS = "chromatograms"
    CLUSTERS = "clusters"
    COMPARISON = "comparison"
    NUCLEOTIDE_SEQUENCES = "nucleotide_sequences"
    PHYLOGENY = "phylogeny"
    PLATE = "plate"
    PROTEIN_SEQUENCES = "protein_sequences"
    READS = "reads"
    REPORT = "report"
    STRUCTURES = "structures"
    TABLE = "table"

    def __str__(self) -> str:
        return str(self.value)
