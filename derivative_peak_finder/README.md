This software identify peaks in a one dimensional signal array, using the principle of the zero equivalent derivative of the curve at the local maximum.
To overcome the signal noise, the derivative is smoothed by the Savitzky-Golay filter.

Examples:

Signal derivative:

![peak_finder_2](https://user-images.githubusercontent.com/59908809/140632617-d0115232-bba2-4751-9778-d38cdbe9107a.png)

Final output:

![peak_finder_1](https://user-images.githubusercontent.com/59908809/140632621-05d190ad-79b3-4a87-8d22-f73264b201cb.png)

The algorithm is inspired by the methods approached in the "A Pragmatic Introduction to Signal Processing
 with applications in scientific measurement" book by Tom O'Haver. https://terpconnect.umd.edu/~toh/spectrum/
 
