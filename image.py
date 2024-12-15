from PIL import Image
import math
import os
import imageio as imageio


images = []
locks = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def swap_pixels(im, n, x, y):
    temp = im.getpixel((n, x))
    im.putpixel((n, x), im.getpixel((n, y)))
    im.putpixel((n, y), temp)
    return im


def swap_rows(im, row1, row2):
    n = im.size[0] - 1
    for j in range(n):
        temp = im.getpixel((j, row1))
        im.putpixel((j, row1), im.getpixel((j, row2)))
        im.putpixel((j, row2), temp)
    return im


def swap_columns(im, col1, col2):
    n = im.size[1] - 1
    for j in range(n):
        temp = im.getpixel((col1, j))
        im.putpixel((col1, j), im.getpixel((col2, j)))
        im.putpixel((col2, j), temp)
    return im


def merge(im, n, respectToAxis, left, right, progress, total_merges):
    """Merge two sorted subarrays into a single sorted array."""
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][0] <= right[j][0]:
            merged.append(left[i])
            if respectToAxis == 0:
                swap_pixels(im, n, left[i][1], right[j][1])
            elif respectToAxis == 1:
                swap_pixels(im, n, left[i][1], right[j][1])
            i += 1
        else:
            merged.append(right[j])
            if respectToAxis == 0:
                swap_pixels(im, n, right[j][1], left[i][1])
            elif respectToAxis == 1:
                swap_pixels(im, n, right[j][1], left[i][1])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    # Update progress
    progress[0] += 1
    percent_complete = (progress[0] / total_merges) * 100
    print(f"Progress: [{'#' * math.ceil(percent_complete / 5)}{'.' * (20 -
          math.ceil(percent_complete / 5))}] {percent_complete:.2f}% completed", end="\r")

    return merged


def merge_sort_with_status(im, n, respectToAxis, arr, progress, total_merges):
    """Perform a merge sort with a status bar."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    sorted_left = merge_sort_with_status(
        im, n, respectToAxis, left, progress, total_merges)
    sorted_right = merge_sort_with_status(
        im, n, respectToAxis, right, progress, total_merges)

    return merge(im, n, respectToAxis, sorted_left, sorted_right, progress, total_merges)


def calculate_total_merges(im, n):
    """Calculate the total number of merge operations required."""
    total = 0
    size = 1
    while size < n:
        total += math.ceil(n / (2 * size))
        size *= 2
    return total * im.size[0]-1


'''
parameters (im, respectToAxis, repectToColor)
im - Image
respectToAxis -
    0 = x axis
    1 = y axis
respectToColor -
    0 = red
    1 = green
    2 = blue
'''


def leftRight(im, respectToAxis, respectToColor):
    n = im.size[respectToAxis] - 1
    total_steps = (n - 1)
    completed_steps = 0

    if respectToAxis == 0:
        for j in range(n):
            if im.getpixel((j, n/2))[respectToColor] > im.getpixel((n-j, 0))[respectToColor]:
                im = swap_columns(im, j, n-j)
            completed_steps += 1
            percent_done = (completed_steps / total_steps) * 100
            print(f"Progress: {percent_done:.2f}%", end="\r")
    elif respectToAxis == 1:
        for j in range(n):
            if im.getpixel((0, j))[respectToColor] > im.getpixel((0, n-j))[respectToColor]:
                im = swap_rows(im, j, n-j)
            completed_steps += 1
            percent_done = (completed_steps / total_steps) * 100
            print(f"Progress: {percent_done:.2f}%", end="\r")

    return im


def create_array(im, respectToAxis, respectToColor):
    n = im.size[respectToAxis] - 1
    mid = n/2
    arr = []
    for i in range(n):
        if respectToColor == -1:
            if respectToAxis == 0:
                average_color_value = im.getpixel((i, mid))[0]
                average_color_value += im.getpixel((i, mid))[1]
                average_color_value += im.getpixel((i, mid))[2]
                average_color_value /= 3
                arr.append(average_color_value)
            elif respectToAxis == 1:
                average_color_value = im.getpixel((mid, i))[0]
                average_color_value += im.getpixel((mid, i))[1]
                average_color_value += im.getpixel((mid, i))[2]
                average_color_value /= 3
                arr.append(average_color_value)
        else:
            if respectToAxis == 0:
                arr.append(im.getpixel((i, n/2))[respectToColor])
            elif respectToAxis == 1:
                arr.append(im.getpixel((n/2, i))[respectToColor])
    return arr


def create_array2(im, respectToColor):
    width = im.size[0] - 1
    height = im.size[1] - 1
    arr = []
    for i in range(width):
        arrtemp = []
        for j in range(height):
            if respectToColor == -1:
                average_color_value = im.getpixel((i, j))[0]
                average_color_value += im.getpixel((i, j))[1]
                average_color_value += im.getpixel((i, j))[2]
                average_color_value /= 3
                arrtemp.append(average_color_value)
            else:
                arrtemp.append(im.getpixel((i, j))[respectToColor])
        foo = [(value, index) for index, value in enumerate(arrtemp)]
        arr.append(foo)
    return arr


def cal_avg(arr):
    avg = 0
    for i in range(len(arr)):
        avg += arr[i]
    return avg / len(arr)


def pixelate(im):
    width, height = im.size
    pixel_size = 2**4
    im = im.resize((width // pixel_size, height //
                   pixel_size), Image.Resampling.NEAREST)
    im = im.resize((width, height), Image.Resampling.NEAREST)
    return im


def save_gif_image(im, percent_complete):
    if (math.ceil(percent_complete) % 10 == 5) and locks[locks[0]] == 1:
        locks[0] += 1
    if (math.ceil(percent_complete) % 10) == 0 and locks[locks[0]] == 0:
        locks[locks[0]] = 1
        pixel_im = im.copy()
        pixel_im = pixelate(pixel_im)
        if locks[locks[0]] != 10:
            pixel_im.save(f"gif_images/{locks[0]}.png")


def main(filePath, respectToAxis, respectToColor):
    with Image.open(filePath) as im:
        # ------------BEGIN STATS----------------
        arr = create_array2(im, respectToColor)

        # avg = cal_avg(arr)
        # print("AVERAGE: ", avg)

        # ------------SORT----------------
        print("STARTING SORT...")
        progress = [0]
        total_steps = calculate_total_merges(im, len(arr[0]))

        n = 0
        for x in arr:
            merge_sort_with_status(im, n, respectToAxis, x,
                                   progress, total_steps)
            n += 1

        # ------------AFTER STATS----------------
        # after_arr = create_array(im, respectToAxis, respectToColor)
        # after_avg = cal_avg(after_arr)
        # print("\nAFTER AVERAGE: ", after_avg)

        # ------------SAVE----------------
        print("IMAGE CREATED oi.png")
        im.save("oi.png")
        file = "sounds/note.mp3"
        os.system("afplay " + file)


if __name__ == "__main__":
    main("images/originals/corridor_bluered.png", 0, -1)
