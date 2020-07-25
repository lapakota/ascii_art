import unittest

from AsciiGenerator import convertToAscii, GRAYSCALE_10, GRAYSCALE_40, \
    parse_args, check_mode, check_width_and_height, create_ascii_image
from PIL import Image


class MyTestCase(unittest.TestCase):

    def test_ascii_converter(self):
        self.assertEqual(len(convertToAscii(
            Image.open("test.jpg"), 100, 50, GRAYSCALE_10)), 5049)
        self.assertEqual(len(convertToAscii(
            Image.open("test.jpg"), 50, 50, GRAYSCALE_40)), 2549)
        self.assertEqual(len(convertToAscii(
            Image.open("test.jpg"), 50, 100, GRAYSCALE_10)), 5099)

    def test_parser(self):
        args = parse_args(['--image', 'test.jpg',
                           '--width', '100',
                           '--height', '50'])
        self.assertTrue(args.image, "test.jpg")
        self.assertTrue(args.width, "100")
        self.assertTrue(args.height, "50")

    def test_args_mode(self):
        args1 = parse_args(['--image', 'test.jpg',
                            '--width', '100',
                            '--height', '50', '--mode', '10'])
        args3 = parse_args(['--image', 'test.jpg',
                            '--width', '100',
                            '--height', '50', '--mode', '40'])
        args5 = parse_args(['--image', 'test.jpg',
                            '--width', '100',
                            '--height', '50', '--mode', '90'])
        args6 = parse_args(['--image', 'test.jpg',
                            '--width', '100',
                            '--height', '50'])
        self.assertEqual(check_mode(args1), GRAYSCALE_10)
        self.assertEqual(check_mode(args3), GRAYSCALE_40)
        self.assertFalse(check_mode(args5))
        self.assertEqual(check_mode(args6), GRAYSCALE_40)

    def test_args_width_and_height(self):
        args1 = parse_args(['--image', 'test.jpg',
                            '--width', '100',
                            '--height', '50'])
        args2 = parse_args(['--image', 'test.jpg',
                            '--width', '0',
                            '--height', '50'])
        args3 = parse_args(['--image', 'test.jpg',
                            '--width', '100',
                            '--height', '0'])
        self.assertEqual(check_width_and_height(
            int(args1.width), int(args1.height)), True)
        self.assertEqual(check_width_and_height(
            int(args2.width), int(args2.height)), False)
        self.assertEqual(check_width_and_height(
            int(args3.width), int(args3.height)), False)

    def test_ascii_image(self):
        args1 = parse_args(['--image', 'test.jpg',
                            '--width', '10',
                            '--height', '5'])
        args2 = parse_args(['--image', 'test.jpg',
                            '--width', '20',
                            '--height', '10'])
        self.assertEqual(create_ascii_image(
            Image.open(args1.image),
            int(args1.width), int(args1.height),
            GRAYSCALE_10).size, (110, 85))
        self.assertEqual(create_ascii_image(
            Image.open(args2.image),
            int(args2.width), int(args2.height),
            GRAYSCALE_40).size, (220, 170))

    def test_ansi_check(self):
        args1 = parse_args(['--image', '256.ansi'])
        args2 = parse_args(['--image', '256.ansi',
                            '--width', '20',
                            '--height', '10'])
        self.assertTrue(check_mode(args1))
        self.assertTrue(check_mode(args2))


if __name__ == '__main__':
    unittest.main()
