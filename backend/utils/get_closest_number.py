def get_closest_num(nums: list[int], target_num: int):
    min_difference_index = 0

    for index in range(len(nums)):
        if abs(nums[index] - target_num) < abs(nums[min_difference_index] - target_num):
            min_difference_index = index

    return nums[min_difference_index]

