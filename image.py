from PIL import Image
import math
import os
import imageio as imageio


images = []
locks = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


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


def merge(im, respectToAxis, left, right, progress, total_merges):
    """Merge two sorted subarrays into a single sorted array."""
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            if respectToAxis == 0:
                swap_rows(im, i, j)
            elif respectToAxis == 1:
                swap_columns(im, i, j)
            i += 1
        else:
            merged.append(right[j])
            '''
            if respectToAxis == 0:
                swap_rows(im, j, i)
            elif respectToAxis == 1:
                swap_columns(im, j, i)
            '''
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    # Update progress
    progress[0] += 1
    percent_complete = (progress[0] / total_merges) * 100
    print(f"Progress: [{'#' * math.ceil(percent_complete / 5)}{'.' * (20 -
          math.ceil(percent_complete / 5))}] {percent_complete:.2f}% completed", end="\r")
    save_gif_image(im, percent_complete)

    return merged


def merge_sort_with_status(im, respectToAxis, arr, progress, total_merges):
    """Perform a merge sort with a status bar."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    sorted_left = merge_sort_with_status(
        im, respectToAxis, left, progress, total_merges)
    sorted_right = merge_sort_with_status(
        im, respectToAxis, right, progress, total_merges)

    return merge(im, respectToAxis, sorted_left, sorted_right, progress, total_merges)


def calculate_total_merges(n):
    """Calculate the total number of merge operations required."""
    total = 0
    size = 1
    while size < n:
        total += math.ceil(n / (2 * size))
        size *= 2
    return total


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
        arr = create_array(im, respectToAxis, respectToColor)
        avg = cal_avg(arr)
        print("AVERAGE: ", avg)

        # ------------SORT----------------
        print("STARTING SORT...")
        progress = [0]
        total_steps = calculate_total_merges(len(arr))
        merge_sort_with_status(im, respectToAxis, arr,
                               progress, total_steps)

        # ------------AFTER STATS----------------
        after_arr = create_array(im, respectToAxis, respectToColor)
        after_avg = cal_avg(after_arr)
        print("\nAFTER AVERAGE: ", after_avg)

        # ------------SAVE----------------
        im.save("oi.png")
        im = pixelate(im)
        im.save("gif_images/10.png")
        im1 = Image.open("gif_images/1.png")
        im2 = Image.open("gif_images/2.png")
        im3 = Image.open("gif_images/3.png")
        im4 = Image.open("gif_images/4.png")
        im5 = Image.open("gif_images/5.png")
        im6 = Image.open("gif_images/6.png")
        im7 = Image.open("gif_images/7.png")
        im8 = Image.open("gif_images/8.png")
        im9 = Image.open("gif_images/9.png")
        im10 = Image.open("gif_images/10.png")
        images = []
        images.extend([im1, im2, im3, im4, im5, im6, im7, im8, im9, im10])
        print(images)
        imageio.mimsave("images/gifs/oig.gif", images, duration=0.5)
        print("IMAGE CREATED oi.png")
        file = "sounds/note.mp3"
        os.system("afplay " + file)


if __name__ == "__main__":
    main("images/originals/yogo_original.png", 1, -1)
