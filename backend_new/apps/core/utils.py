"""
Utility functions
"""
import os
from uuid import uuid4


def get_file_path(instance, filename):
    """
    Generate unique file path for uploads
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('uploads', filename)


def to_persian_number(number):
    """
    Convert English numbers to Persian numerals
    """
    persian_digits = {
        '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
        '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
    }
    return ''.join(persian_digits.get(ch, ch) for ch in str(number))


def to_english_number(number_str):
    """
    Convert Persian numerals to English numbers
    """
    english_digits = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
    }
    return ''.join(english_digits.get(ch, ch) for ch in str(number_str))
