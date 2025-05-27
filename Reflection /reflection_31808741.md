# Personal Reflection on Data Encoding

## 1.Description

In this project, I was primarily responsible for implementing the core QR code encoding logic. This included string analysis, data encoding in different modes (numeric, alphanumeric, byte), and generating the final bit stream. I also developed the module that structures the encoded data and error correction codewords into a final binary stream before matrix placement.

## 2.Feelings

Initially, I felt a bit overwhelmed by the complexity of the QR code specification. However, as I broke down the tasks into smaller components and tested them incrementally, I gained more confidence and satisfaction in seeing the encoding work correctly.

## 3.Evaluation

The encoding modules functioned correctly and aligned with the QR specification. The data was well-structured, and error correction codewords were integrated successfully. However, the Kanji mode was left unimplemented, and the analyse function only supported single-mode encoding, which limited flexibility.

## 4.Analysis

Developing this functionality improved my skills in binary operations and Python modular design. Key technical challenges included precise bit alignment and correct grouping of data. I also realized the importance of early validation when debugging interleaving logic for data and ECC codewords

## 5.Conclusions

Overall, my implementation contributed significantly to the project’s success. It showed that breaking down specifications and incremental development are effective strategies. However, the work remains incomplete without full mode support and deeper optimization strategies.

## 6.Action Plan

If I revisit this project, I plan to implement full Kanji mode support and extend the analyse function to allow mixed-mode encoding for better efficiency. I also intend to create a visualizer to display intermediate bit streams for easier debugging and understanding of the encoding process.
