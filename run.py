from setup import llm_chain

def main():
    print("Welcome to the Footballer Recommendation System!")
    print("----------------------------------------")
    
    while True:
        try:
            user_query = input("\nWhat types of footballers are you looking for? (or 'quit' to exit): ")
            
            if user_query.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using the Footballer Recommendation System!")
                break
                
            if not user_query.strip():
                print("Please enter a valid query.")
                continue
                
            print("\nGenerating recommendations...")
            result = llm_chain(user_query)
            print("\nRecommendations:")
            print("---------------")
            print(result)
            
        except KeyboardInterrupt:
            print("\n\nExiting the Footballer Recommendation System. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main() 