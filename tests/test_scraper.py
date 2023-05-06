import unittest

from modules.scraper import ScrapePAA


class TestScrapePAA(unittest.TestCase):

    def setUp(self):
        self.scraper = ScrapePAA()
        self.scraper.open_page("https://google.com")

    def test_scrape_people_also_ask(self):
        expected_questions = [
            # Add a list of expected questions based on the sample HTML content
        ]

        self.scraper.search_query_browser("chicken", first_search=False)
        all_questions =self.scraper.scrape_people_also_ask()
        self.assertTrue(len(all_questions) > 0)

    def test_scrape_link_results(self):
        self.scraper.driver.page_source = '''<your sample HTML content here>'''

        expected_links = [
            # Add a list of expected links based on the sample HTML content
        ]

        actual_links = self.scraper.scrape_link_results()
        self.assertEqual(expected_links, actual_links)

    # Add more test cases as needed
    def tearDown(self):
        self.scraper.driver.quit()

if __name__ == '__main__':
    unittest.main()
