from backend.database import get_supabase


def test_connection():
    print("Connecting to ReLoop Supabase...")

    supabase = get_supabase()

    response = (
        supabase.table("materials")
        .select("id")
        .limit(1)
        .execute()
    )

    print("Connection successful!")
    print("Materials found:", len(response.data))


if __name__ == "__main__":
    test_connection()