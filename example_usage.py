from client import SparkpageSynthesisEngineClient

def main():
    client = SparkpageSynthesisEngineClient()
    res = client.synthesize_page()
    print("=== Sparkpage Synthesis Engine Output ===")
    print(f"Winner: {res['winner_name']} (Score: {res['winner_score']}/10.0)")
    print(f"Total Evaluated: {res['total_evaluated']}")
    print("\nMarkdown Table:\n" + res['comparison_table_markdown'])

if __name__ == '__main__':
    main()
