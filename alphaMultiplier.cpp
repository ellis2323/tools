#include <iostream>
#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image.h"
#include "stb_image_write.h"

int main(int argc, char *argv[]) {
   if (argc != 3) {
        std::cerr << "Usage: alphaMultiplier <file_in> <file_out>" << std::endl;
		return -1;
    }
    const char* file_in = argv[1];
    const char* file_out = argv[2];
    // load
    int width, height, n;
    unsigned char *data = stbi_load(file_in, &width, &height, &n, 4);
    if (data == nullptr) {
        std::cerr << file_in << " not a png" << std::endl;
        return -1;
    }
    std::cout << "premultiply " << file_in << " width:" << width << " height:" << height << " component:" << n << std::endl;
    // premultiply
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            unsigned char* ptr = &(data[(width*y+x)*4]);
            int r = ptr[0];
            int g = ptr[1];
            int b = ptr[2];
            r = (r * ptr[3]) >> 8;
            g = (g * ptr[3]) >> 8;
            b = (b * ptr[3]) >> 8;
            ptr[0] = r;
            ptr[1] = g;
            ptr[2] = b;
        }
    }
    // write result
    stbi_write_png(file_out, width, height, 4, data, width * 4);
	return 0;
}
