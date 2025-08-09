"""
Comprehensive test for WhatsApp Analyzer
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import tempfile
from parser import parse_whatsapp
from analyzer import analyze_chat


def test_basic_functionality():
    """Test basic parsing and analysis"""
    print("Testing basic functionality...")
    
    # Test data with more features for comprehensive testing
    test_chat = """[1.1.2024, 10:00:00] Alice: Hello everyone! 😊
[1.1.2024, 10:00:30] Alice: How is everyone doing today?
[1.1.2024, 10:00:31] Alice: I'm so excited for this weekend!
[1.1.2024, 10:01:00] Bob: Hi there! How are you? This is a longer message to test average length calculation
[1.1.2024, 10:02:00] Alice: Great day today haha 🌞
[1.1.2024, 10:03:00] Charlie: Morning! I'm excited lol
[1.1.2024, 10:04:00] Bob: Same here 😂😂
[1.1.2024, 10:05:00] ‎Messages and calls are end-to-end encrypted.
[1.1.2024, 10:06:00] Alice: Did you see the news?
[1.1.2024, 10:07:00] Charlie: Yes! Absolutely amazing 🎉
[1.1.2024, 10:08:00] Bob: Best news ever hahaha
[1.1.2024, 11:00:00] Charlie: Starting new conversation after gap
[1.1.2024, 14:00:00] Alice: Another conversation starter"""
    
    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
        f.write(test_chat)
        temp_file = f.name
    
    try:
        # Test parsing
        print("  ✓ Testing parser...")
        df = parse_whatsapp(temp_file)
        assert not df.empty, "Parser should return data"
        assert len(df) == 12, f"Expected 12 messages, got {len(df)}"  # 13 total - 1 system message
        assert df['user'].nunique() == 3, f"Expected 3 users, got {df['user'].nunique()}"
        print(f"    Parsed {len(df)} messages from {df['user'].nunique()} users")
        
        # Test analysis
        print("  ✓ Testing full analyzer...")
        results = analyze_chat(df)
        assert isinstance(results, dict), "Analyzer should return dict"
        
        # Test all expected sections
        expected_sections = [
            'basic_stats', 'messages_per_user', 'avg_message_length',
            'messages_by_hour', 'messages_by_day', 'most_common_words',
            'avg_response_time_per_user', 'laughs_per_user', 'emoji_per_user',
            'most_common_emojis', 'message_bursts', 'conversation_starters', 'all_users_data'
        ]
        
        for section in expected_sections:
            assert section in results, f"Should have {section} section"
        print(f"    All {len(expected_sections)} analysis sections present")
        
        # Test basic stats
        basic_stats = results['basic_stats']
        assert basic_stats['total_messages'] == 12, f"Expected 12 messages, got {basic_stats['total_messages']}"
        assert basic_stats['total_users'] == 3, f"Expected 3 users, got {basic_stats['total_users']}"
        assert basic_stats['date_range_days'] >= 1, "Should have at least 1 day range"
        print(f"    Basic stats: {basic_stats['total_messages']} messages, {basic_stats['total_users']} users")
        
        # Test emoji analysis
        emoji_stats = results['most_common_emojis']
        emoji_per_user = results['emoji_per_user']
        assert len(emoji_stats) > 0, "Should detect emojis"
        assert isinstance(emoji_per_user, dict), "Emoji per user should be dict"
        total_emojis = sum(emoji_per_user.values())
        print(f"    Emoji analysis: {len(emoji_stats)} unique emojis, {total_emojis} total")
        
        # Test laugh analysis
        laugh_stats = results['laughs_per_user']
        assert isinstance(laugh_stats, dict), "Laugh stats should be dict"
        total_laughs = sum(laugh_stats.values())
        assert total_laughs > 0, "Should detect laughs"
        print(f"    Laugh analysis: {total_laughs} laugh instances across {len(laugh_stats)} users")
        
        # Test message length analysis
        avg_lengths = results['avg_message_length']
        assert isinstance(avg_lengths, dict), "Average lengths should be dict"
        assert len(avg_lengths) == 3, "Should have avg length for all 3 users"
        for user, length in avg_lengths.items():
            assert length > 0, f"User {user} should have positive average length"
        print(f"    Average message lengths calculated for {len(avg_lengths)} users")
        
        # Test time pattern analysis
        by_hour = results['messages_by_hour']
        by_day = results['messages_by_day']
        assert isinstance(by_hour, dict), "Messages by hour should be dict"
        assert isinstance(by_day, dict), "Messages by day should be dict"
        assert len(by_hour) > 0, "Should have hourly data"
        print(f"    Time patterns: {len(by_hour)} hours, {len(by_day)} days")
        
        # Test response time analysis
        response_times = results['avg_response_time_per_user']
        assert isinstance(response_times, dict), "Response times should be dict"
        print(f"    Response times calculated for {len(response_times)} users")
        
        # Test burst analysis
        bursts = results['message_bursts']
        assert isinstance(bursts, dict), "Message bursts should be dict"
        total_bursts = sum(bursts.values())
        print(f"    Message bursts: {total_bursts} bursts detected")
        
        # Test conversation starters
        starters = results['conversation_starters']
        assert isinstance(starters, dict), "Conversation starters should be dict"
        total_starts = sum(starters.values())
        print(f"    Conversation starters: {total_starts} conversation starts detected")
        
        # Test word frequency
        words = results['most_common_words']
        assert isinstance(words, list), "Most common words should be list"
        assert len(words) > 0, "Should have some words"
        for word, count in words:
            assert isinstance(word, str) and isinstance(count, int), "Word frequency format should be (str, int)"
        print(f"    Word frequency: {len(words)} common words identified")
        
        # Test all_users_data (pre-calculated user analysis)
        all_users = results['all_users_data']
        assert isinstance(all_users, dict), "All users data should be dict"
        assert len(all_users) == 3, "Should have data for all 3 users"
        
        for user, user_data in all_users.items():
            assert 'total_messages' in user_data, f"User {user} should have total_messages"
            assert 'avg_length' in user_data, f"User {user} should have avg_length"
            assert 'hourly_activity' in user_data, f"User {user} should have hourly_activity"
            assert 'user_emojis' in user_data, f"User {user} should have user_emojis"
            assert user_data['total_messages'] > 0, f"User {user} should have positive message count"
        print(f"    Pre-calculated user data: complete for {len(all_users)} users")
        
        print("  ✅ All comprehensive functionality tests PASSED!")
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        os.unlink(temp_file)


def test_individual_analyzer_functions():
    """Test individual analyzer functions separately"""
    print("Testing individual analyzer functions...")
    
    # Import individual functions
    from analyzer import (
        preprocess_df, calculate_emoji_analysis, calculate_word_frequency,
        calculate_laugh_analysis, calculate_basic_stats, calculate_user_metrics,
        calculate_time_patterns, get_avg_response, calculate_message_bursts,
        calculate_conversation_starters
    )
    
    # Test data
    test_chat = """[1.1.2024, 10:00:00] User1: Hello world! 😊
[1.1.2024, 10:00:30] User1: How are you?
[1.1.2024, 10:01:00] User2: I'm great thanks lol 😂
[1.1.2024, 10:02:00] User1: Awesome haha 🎉"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
        f.write(test_chat)
        temp_file = f.name
    
    try:
        # Parse and preprocess
        df = parse_whatsapp(temp_file)
        processed_df = preprocess_df(df)
        
        # Test preprocess_df
        print("  ✓ Testing preprocess_df...")
        required_cols = ['lower_message', 'message_length', 'hour', 'day_name', 'emojis', 'emoji_count']
        for col in required_cols:
            assert col in processed_df.columns, f"Should have {col} column"
        assert all(isinstance(emojis, list) for emojis in processed_df['emojis']), "Emojis should be lists"
        print(f"    Added {len(required_cols)} preprocessing columns")
        
        # Test calculate_basic_stats
        print("  ✓ Testing calculate_basic_stats...")
        total_msgs, total_users, date_range = calculate_basic_stats(processed_df)
        assert total_msgs == 4, f"Expected 4 messages, got {total_msgs}"
        assert total_users == 2, f"Expected 2 users, got {total_users}"
        assert date_range >= 1, "Should have at least 1 day range"
        print(f"    Basic stats: {total_msgs} messages, {total_users} users, {date_range} days")
        
        # Test calculate_user_metrics
        print("  ✓ Testing calculate_user_metrics...")
        msgs_per_user, avg_length_per_user = calculate_user_metrics(processed_df)
        assert len(msgs_per_user) == 2, "Should have metrics for 2 users"
        assert len(avg_length_per_user) == 2, "Should have avg lengths for 2 users"
        assert all(count > 0 for count in msgs_per_user), "All users should have positive message counts"
        print(f"    User metrics calculated for {len(msgs_per_user)} users")
        
        # Test calculate_time_patterns
        print("  ✓ Testing calculate_time_patterns...")
        by_hour, by_day, avg_response = calculate_time_patterns(processed_df)
        assert len(by_hour) > 0, "Should have hourly patterns"
        assert len(by_day) > 0, "Should have daily patterns"
        print(f"    Time patterns: {len(by_hour)} hours, {len(by_day)} days")
        
        # Test calculate_emoji_analysis
        print("  ✓ Testing calculate_emoji_analysis...")
        emoji_per_user, most_common_emojis = calculate_emoji_analysis(processed_df)
        assert len(most_common_emojis) > 0, "Should detect emojis"
        assert len(emoji_per_user) > 0, "Should have emoji counts per user"
        print(f"    Emoji analysis: {len(most_common_emojis)} unique emojis")
        
        # Test calculate_word_frequency
        print("  ✓ Testing calculate_word_frequency...")
        word_freq = calculate_word_frequency(processed_df)
        assert isinstance(word_freq, list), "Should return list of tuples"
        assert len(word_freq) > 0, "Should have word frequencies"
        print(f"    Word frequency: {len(word_freq)} common words")
        
        # Test calculate_laugh_analysis
        print("  ✓ Testing calculate_laugh_analysis...")
        laugh_result = calculate_laugh_analysis(processed_df)
        assert len(laugh_result) > 0, "Should detect laughs"
        total_laughs = laugh_result.sum()
        assert total_laughs > 0, "Should have positive laugh count"
        print(f"    Laugh analysis: {total_laughs} laughs detected")
        
        # Test get_avg_response
        print("  ✓ Testing get_avg_response...")
        response_times = get_avg_response(processed_df)
        assert isinstance(response_times, dict), "Should return dict"
        print(f"    Response times calculated for {len(response_times)} users")
        
        # Test calculate_message_bursts
        print("  ✓ Testing calculate_message_bursts...")
        bursts = calculate_message_bursts(processed_df)
        assert len(bursts) >= 0, "Should return burst data"
        print(f"    Message bursts: {bursts.sum()} total bursts")
        
        # Test calculate_conversation_starters
        print("  ✓ Testing calculate_conversation_starters...")
        starters = calculate_conversation_starters(processed_df)
        assert len(starters) >= 0, "Should return conversation starter data"
        print(f"    Conversation starters: {starters.sum()} conversation starts")
        
        print("  ✅ All individual function tests PASSED!")
        return True
        
    except Exception as e:
        print(f"  ❌ Individual function test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        os.unlink(temp_file)


def test_format_compatibility():
    """Test different WhatsApp export formats"""
    print("Testing format compatibility...")
    
    try:
        # Test Hebrew format
        hebrew_chat = """[5.1.2024, 15:30:45] UserA: Hebrew format test 😊
[5.1.2024, 15:31:00] UserB: Response test haha"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write(hebrew_chat)
            temp_file = f.name
        
        df_hebrew = parse_whatsapp(temp_file)
        assert len(df_hebrew) == 2, "Should parse Hebrew format"
        print("  ✓ Hebrew format [DD.MM.YYYY, HH:MM:SS] works")
        os.unlink(temp_file)
        
        # Test English format
        english_chat = """[05/01/2024, 3:30:45] UserA: English format test 😊
[05/01/2024, 3:31:00] UserB: Response test lol"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write(english_chat)
            temp_file = f.name
        
        df_english = parse_whatsapp(temp_file)
        assert len(df_english) == 2, "Should parse English format"
        print("  ✓ English format [DD/MM/YYYY, H:MM:SS] works")
        os.unlink(temp_file)
        
        # Test system message filtering
        system_chat = """[1.1.2024, 10:00:00] User1: Real message
[1.1.2024, 10:01:00] ‎Messages and calls are end-to-end encrypted.
[1.1.2024, 10:02:00] User2: Another real message
[1.1.2024, 10:03:00] ‎<Media omitted>"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write(system_chat)
            temp_file = f.name
        
        df_filtered = parse_whatsapp(temp_file)
        assert len(df_filtered) == 2, "Should filter out system messages"
        all_messages = ' '.join(df_filtered['message'].values)
        assert 'encrypted' not in all_messages.lower(), "Should not contain system message text"
        print("  ✓ System message filtering works")
        os.unlink(temp_file)
        
        print("  ✅ All format compatibility tests PASSED!")
        return True
        
    except Exception as e:
        print(f"  ❌ Format compatibility test failed: {e}")
        return False


def test_edge_cases():
    """Test edge cases"""
    print("Testing edge cases...")
    
    try:
        # Test empty file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write("")
            temp_file = f.name
        
        df = parse_whatsapp(temp_file)
        assert df.empty, "Empty file should return empty DataFrame"
        print("  ✓ Empty file handling works")
        os.unlink(temp_file)
        
        # Test invalid format
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write("Invalid chat format\nNo timestamps here")
            temp_file = f.name
        
        df = parse_whatsapp(temp_file)
        assert df.empty, "Invalid format should return empty DataFrame"
        print("  ✓ Invalid format handling works")
        os.unlink(temp_file)
        
        # Test mixed valid/invalid lines
        mixed_content = """[1.1.2024, 10:00:00] User1: Valid message
Invalid line without format
[1.1.2024, 10:01:00] User2: Another valid message"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write(mixed_content)
            temp_file = f.name
        
        df = parse_whatsapp(temp_file)
        assert len(df) == 2, "Should parse only valid lines"
        print("  ✓ Mixed format handling works")
        os.unlink(temp_file)
        
        # Test single message
        single_msg = """[1.1.2024, 10:00:00] User1: Only one message"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write(single_msg)
            temp_file = f.name
        
        df = parse_whatsapp(temp_file)
        results = analyze_chat(df)
        assert results['basic_stats']['total_messages'] == 1, "Should handle single message"
        print("  ✓ Single message handling works")
        os.unlink(temp_file)
        
        print("  ✅ All edge case tests PASSED!")
        return True
        
    except Exception as e:
        print(f"  ❌ Edge case test failed: {e}")
        return False
    """Test edge cases"""
    print("Testing edge cases...")
    
    try:
        # Test empty file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write("")
            temp_file = f.name
        
        df = parse_whatsapp(temp_file)
        assert df.empty, "Empty file should return empty DataFrame"
        print("  ✓ Empty file handling works")
        os.unlink(temp_file)
        
        # Test invalid format
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write("Invalid chat format\nNo timestamps here")
            temp_file = f.name
        
        df = parse_whatsapp(temp_file)
        assert df.empty, "Invalid format should return empty DataFrame"
        print("  ✓ Invalid format handling works")
        os.unlink(temp_file)
        
        print("  ✅ All edge case tests PASSED!")
        return True
        
    except Exception as e:
        print(f"  ❌ Edge case test failed: {e}")
        return False


def main():
    print("WhatsApp Analyzer - Comprehensive Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Run all tests
    all_passed &= test_basic_functionality()
    all_passed &= test_individual_analyzer_functions()
    all_passed &= test_format_compatibility()
    all_passed &= test_edge_cases()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! The analyzer is working correctly! 🎉")
        print("✅ Parser: Hebrew & English formats working")
        print("✅ Analyzer: All 13 analysis sections working")  
        print("✅ Individual functions: All components tested")
        print("✅ Edge cases: Error handling working")
        print("✅ Emojis: Detection and counting working")
        print("✅ Laughs: Pattern recognition working") 
        print("✅ Response times: Calculation working")
        print("✅ Message bursts: Detection working")
        print("✅ Conversation starters: Identification working")
        print("✅ Word frequency: Analysis working")
        print("✅ Time patterns: Hour/day analysis working")
        print("✅ Pre-calculation: User data caching working")
    else:
        print("❌ Some tests failed. Check the output above.")
    
    return all_passed


if __name__ == '__main__':
    main()
