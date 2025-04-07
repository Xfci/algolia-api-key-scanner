import requests
import time
import json
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def check_api_key(app_id, api_key):
    """Check API key permissions and details"""
    try:
        # Get API key information
        key_url = f"https://{app_id}.algolia.net/1/keys/{api_key}"
        headers = {
            "X-Algolia-API-Key": api_key,
            "X-Algolia-Application-Id": app_id
        }
        
        response = requests.get(key_url, headers=headers)
        
        if response.status_code == 200:
            key_data = response.json()
            return key_data
        else:
            print(f"{Fore.RED}Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        return None

def test_operations(app_id, api_key, index_name):
    """Test what operations the key can perform"""
    operations_result = {
        "can_search": False,
        "can_list_indices": False,
        "can_read_settings": False,
        "can_write": False,
        "can_delete": False
    }
    
    headers = {
        "X-Algolia-API-Key": api_key,
        "X-Algolia-Application-Id": app_id,
        "Content-Type": "application/json"
    }
    
    # Test search
    try:
        search_url = f"https://{app_id}-dsn.algolia.net/1/indexes/{index_name}/query"
        search_data = {"params": "query=&hitsPerPage=1"}
        response = requests.post(search_url, headers=headers, data=json.dumps(search_data))
        operations_result["can_search"] = response.status_code == 200
    except:
        pass
    
    # Test list indices
    try:
        list_url = f"https://{app_id}.algolia.net/1/indexes"
        response = requests.get(list_url, headers=headers)
        operations_result["can_list_indices"] = response.status_code == 200
    except:
        pass
    
    # Test read settings
    try:
        settings_url = f"https://{app_id}.algolia.net/1/indexes/{index_name}/settings"
        response = requests.get(settings_url, headers=headers)
        operations_result["can_read_settings"] = response.status_code == 200
    except:
        pass
    
    # Test write (add object)
    try:
        add_url = f"https://{app_id}.algolia.net/1/indexes/{index_name}"
        test_data = {"objectID": "test_scan_object", "test_field": "This is a test"}
        response = requests.post(add_url, headers=headers, data=json.dumps(test_data))
        operations_result["can_write"] = response.status_code in [200, 201]
    except:
        pass
    
    # Test delete (delete object) - only if we could write
    if operations_result["can_write"]:
        try:
            delete_url = f"https://{app_id}.algolia.net/1/indexes/{index_name}/test_scan_object"
            response = requests.delete(delete_url, headers=headers)
            operations_result["can_delete"] = response.status_code == 200
        except:
            pass
    
    return operations_result

def analyze_permissions(acl):
    """Analyze ACL permissions and describe them in plain English"""
    descriptions = []
    
    if "*" in acl:
        descriptions.append(f"{Fore.RED}This key has FULL ADMIN access with unrestricted permissions")
        return descriptions
    
    permission_descriptions = {
        "search": "Can perform search operations",
        "browse": "Can browse all objects in an index",
        "addObject": "Can add new objects to an index",
        "deleteObject": "Can delete objects from an index",
        "deleteIndex": "Can delete entire indices",
        "settings": "Can read index settings",
        "editSettings": "Can modify index settings",
        "analytics": "Can access analytics data",
        "listIndexes": "Can list all indices",
        "logs": "Can access API logs",
        "recommendation": "Can use recommendation features",
        "usage": "Can view usage data",
        "restrictIndices": "Has restrictions on which indices it can access",
        "restrictSources": "Has restrictions on API request sources"
    }
    
    for permission in acl:
        if permission in permission_descriptions:
            descriptions.append(permission_descriptions[permission])
        else:
            descriptions.append(f"Has '{permission}' permission")
            
    if "addObject" in acl or "deleteObject" in acl or "deleteIndex" in acl:
        descriptions.append(f"{Fore.YELLOW}Warning: This key has write/delete permissions")
            
    return descriptions

def display_results(key_data, operations_result=None):
    """Display key information and permissions analysis"""
    print("\n" + "="*50)
    print(f"{Fore.CYAN}ALGOLIA API KEY ANALYSIS")
    print("="*50)
    
    # Display when the key was created
    created_date = datetime.fromtimestamp(key_data.get("createdAt", 0))
    print(f"\n{Fore.BLUE}Key Creation Date: {Fore.WHITE}{created_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Display validity if it exists
    validity = key_data.get("validity", 0)
    if validity > 0:
        expiry_date = datetime.fromtimestamp(key_data.get("createdAt", 0) + validity)
        print(f"{Fore.BLUE}Key Expiry Date: {Fore.WHITE}{expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"{Fore.BLUE}Key Expiry: {Fore.WHITE}Never (no expiration)")
    
    # Display description if it exists
    if "description" in key_data and key_data["description"]:
        print(f"{Fore.BLUE}Key Description: {Fore.WHITE}{key_data['description']}")
    
    # Display ACL permissions
    acl = key_data.get("acl", [])
    print(f"\n{Fore.BLUE}ACL Permissions:")
    print(f"{Fore.WHITE}{', '.join(acl)}")
    
    # Check if this is an admin key
    is_admin = "*" in acl
    if is_admin:
        print(f"\n{Fore.RED}⚠️  VULNERABLE: This is an admin API key with full permissions ⚠️")
    
    # Display permission analysis
    print(f"\n{Fore.BLUE}Permission Analysis:")
    for desc in analyze_permissions(acl):
        print(f"- {desc}")
    
    # Display operation test results if available
    if operations_result:
        print(f"\n{Fore.BLUE}Operation Tests:")
        for op, result in operations_result.items():
            status = f"{Fore.GREEN}Yes" if result else f"{Fore.RED}No"
            print(f"- {op.replace('_', ' ').title()}: {status}")
    
    print("\n" + "="*50)
    
    return acl, operations_result

def search_objects(app_id, api_key, index_name):
    """Search for objects in the index"""
    try:
        headers = {
            "X-Algolia-API-Key": api_key,
            "X-Algolia-Application-Id": app_id,
            "Content-Type": "application/json"
        }
        
        query = input(f"\n{Fore.YELLOW}Enter search query (leave empty for all): ")
        limit = input(f"{Fore.YELLOW}Enter number of results to return (default 10): ")
        
        if not limit:
            limit = 10
        else:
            limit = int(limit)
        
        search_url = f"https://{app_id}-dsn.algolia.net/1/indexes/{index_name}/query"
        search_data = {"params": f"query={query}&hitsPerPage={limit}"}
        
        print(f"\n{Fore.CYAN}Searching for objects...")
        response = requests.post(search_url, headers=headers, data=json.dumps(search_data))
        
        if response.status_code == 200:
            results = response.json()
            hits = results.get("hits", [])
            print(f"\n{Fore.GREEN}Found {len(hits)} objects:")
            
            # Check if we have the name attribute in the hits
            has_name = any("name" in hit for hit in hits[:5]) if hits else False
            
            for i, hit in enumerate(hits, 1):
                print(f"\n{Fore.CYAN}Result {i}:")
                print(f"{Fore.BLUE}Object ID: {Fore.WHITE}{hit.get('objectID', 'N/A')}")
                
                # Show the name if available
                if "name" in hit:
                    print(f"{Fore.BLUE}Name: {Fore.WHITE}{hit.get('name', 'N/A')}")
                
                # If there's a title but no name, show that
                elif "title" in hit:
                    print(f"{Fore.BLUE}Title: {Fore.WHITE}{hit.get('title', 'N/A')}")
                
                # Try to find a name-like field
                else:
                    name_fields = ["productName", "display_name", "displayName", "product_name", "item_name", "label"]
                    for field in name_fields:
                        if field in hit:
                            print(f"{Fore.BLUE}{field}: {Fore.WHITE}{hit.get(field, 'N/A')}")
                            break
                
                # Show a few key fields
                keys = list(hit.keys())
                if len(keys) > 1:
                    print(f"{Fore.BLUE}Fields: {Fore.WHITE}{', '.join(keys[:5])}" + (f" and {len(keys)-5} more..." if len(keys) > 5 else ""))
                    
                    # Show a sample of the data
                    print(f"{Fore.BLUE}Sample data:")
                    count = 0
                    for k, v in hit.items():
                        if k != "objectID" and k != "name" and k != "title" and count < 3:
                            if isinstance(v, str) and len(v) > 50:
                                v = v[:50] + "..."
                            print(f"  {k}: {v}")
                            count += 1
            
            return True
        else:
            print(f"{Fore.RED}Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        return False

def list_indices(app_id, api_key):
    """List all indices"""
    try:
        headers = {
            "X-Algolia-API-Key": api_key,
            "X-Algolia-Application-Id": app_id
        }
        
        list_url = f"https://{app_id}.algolia.net/1/indexes"
        
        print(f"\n{Fore.CYAN}Listing indices...")
        response = requests.get(list_url, headers=headers)
        
        if response.status_code == 200:
            results = response.json()
            items = results.get("items", [])
            print(f"\n{Fore.GREEN}Found {len(items)} indices:")
            
            for i, item in enumerate(items, 1):
                name = item.get('name', 'N/A')
                print(f"{Fore.CYAN}{i}. {Fore.WHITE}{name}")
                print(f"   {Fore.BLUE}Entries: {Fore.WHITE}{item.get('entries', 'N/A')}")
                print(f"   {Fore.BLUE}Created: {Fore.WHITE}{datetime.fromtimestamp(item.get('createdAt', 0)).strftime('%Y-%m-%d')}")
                print(f"   {Fore.BLUE}Updated: {Fore.WHITE}{datetime.fromtimestamp(item.get('updatedAt', 0)).strftime('%Y-%m-%d')}")
                
                # Try to fetch and display the first object to get an idea of structure
                if operations_result["can_search"]:
                    try:
                        search_url = f"https://{app_id}-dsn.algolia.net/1/indexes/{name}/query"
                        search_data = {"params": "query=&hitsPerPage=1"}
                        obj_response = requests.post(search_url, headers={**headers, "Content-Type": "application/json"}, data=json.dumps(search_data))
                        
                        if obj_response.status_code == 200:
                            obj_results = obj_response.json()
                            hits = obj_results.get("hits", [])
                            
                            if hits:
                                first_obj = hits[0]
                                # Print object name if available
                                if "name" in first_obj:
                                    print(f"   {Fore.BLUE}Sample object name: {Fore.WHITE}{first_obj.get('name')}")
                                elif "title" in first_obj:
                                    print(f"   {Fore.BLUE}Sample object title: {Fore.WHITE}{first_obj.get('title')}")
                                
                                # List available fields
                                fields = list(first_obj.keys())
                                print(f"   {Fore.BLUE}Object fields: {Fore.WHITE}{', '.join(fields[:5])}" + (f" and {len(fields)-5} more..." if len(fields) > 5 else ""))
                    except Exception as e:
                        pass  # Silently fail if we can't get sample object
            
            return True
        else:
            print(f"{Fore.RED}Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        return False

def get_settings(app_id, api_key, index_name):
    """Get index settings"""
    try:
        headers = {
            "X-Algolia-API-Key": api_key,
            "X-Algolia-Application-Id": app_id
        }
        
        settings_url = f"https://{app_id}.algolia.net/1/indexes/{index_name}/settings"
        
        print(f"\n{Fore.CYAN}Getting index settings...")
        response = requests.get(settings_url, headers=headers)
        
        if response.status_code == 200:
            settings = response.json()
            print(f"\n{Fore.GREEN}Index Settings:")
            
            # Display important settings
            important_settings = [
                "searchableAttributes", "attributesForFaceting", "ranking", 
                "customRanking", "replicas", "slaves", "queryLanguages"
            ]
            
            for setting in important_settings:
                if setting in settings:
                    print(f"\n{Fore.BLUE}{setting}:")
                    value = settings[setting]
                    if isinstance(value, list):
                        for item in value:
                            print(f"  - {item}")
                    else:
                        print(f"  {value}")
            
            # Ask if user wants to see all settings
            see_all = input(f"\n{Fore.YELLOW}Do you want to see all settings? (y/n): ").lower() == 'y'
            
            if see_all:
                print(f"\n{Fore.GREEN}All Settings:")
                print(json.dumps(settings, indent=2))
            
            return True
        else:
            print(f"{Fore.RED}Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        return False

def delete_object(app_id, api_key, index_name):
    """Delete an object from the index"""
    try:
        headers = {
            "X-Algolia-API-Key": api_key,
            "X-Algolia-Application-Id": app_id
        }
        
        object_id = input(f"\n{Fore.YELLOW}Enter the objectID to delete: ")
        
        if not object_id:
            print(f"{Fore.RED}Error: ObjectID cannot be empty")
            return False
        
        # URL encode the object ID
        object_id_encoded = object_id.replace("/", "%2F")
        delete_url = f"https://{app_id}.algolia.net/1/indexes/{index_name}/{object_id_encoded}"
        
        # Confirm deletion
        confirm = input(f"\n{Fore.RED}Are you sure you want to delete object '{object_id}'? (yes/no): ").lower()
        if confirm != 'yes':
            print(f"{Fore.YELLOW}Deletion cancelled.")
            return False
        
        print(f"\n{Fore.CYAN}Deleting object...")
        response = requests.delete(delete_url, headers=headers)
        
        if response.status_code == 200:
            print(f"\n{Fore.GREEN}Object deleted successfully!")
            print(f"{Fore.BLUE}Response: {response.json()}")
            return True
        else:
            print(f"{Fore.RED}Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        return False

def main():
    print(f"{Fore.CYAN}Algolia API Key Scanner")
    print(f"{Fore.CYAN}====================")
    
    app_id = input(f"{Fore.YELLOW}Enter Algolia App ID: ")
    api_key = input(f"{Fore.YELLOW}Enter Algolia API Key: ")
    index_name = input(f"{Fore.YELLOW}Enter Algolia Index Name: ")
    
    print(f"\n{Fore.CYAN}Starting scan...")
    
    # Check key permissions
    key_data = check_api_key(app_id, api_key)
    
    if key_data:
        # Test operations
        global operations_result
        operations_result = test_operations(app_id, api_key, index_name)
        
        # Display results
        acl, operations = display_results(key_data, operations_result)
        
        # Show available actions based on permissions
        available_actions = []
        
        if operations["can_search"]:
            available_actions.append(("1", "Search objects"))
        
        if operations["can_list_indices"]:
            available_actions.append(("2", "List indices"))
        
        if operations["can_read_settings"]:
            available_actions.append(("3", "Get index settings"))
        
        if operations["can_delete"]:
            available_actions.append(("4", "Delete object"))
        
        if available_actions:
            while True:
                print(f"\n{Fore.CYAN}Available Actions:")
                for action_id, action_name in available_actions:
                    print(f"{Fore.GREEN}{action_id}. {Fore.WHITE}{action_name}")
                print(f"{Fore.GREEN}q. {Fore.WHITE}Quit")
                
                choice = input(f"\n{Fore.YELLOW}What do you want to do? ")
                
                if choice == "q":
                    break
                
                action_map = {action_id: action_name for action_id, action_name in available_actions}
                
                if choice in action_map:
                    if choice == "1":
                        search_objects(app_id, api_key, index_name)
                    elif choice == "2":
                        list_indices(app_id, api_key)
                    elif choice == "3":
                        get_settings(app_id, api_key, index_name)
                    elif choice == "4":
                        delete_object(app_id, api_key, index_name)
                else:
                    print(f"{Fore.RED}Invalid choice!")
        else:
            print(f"\n{Fore.RED}No actions available with this API key.")
    else:
        print(f"{Fore.RED}Failed to retrieve API key information.")

if __name__ == "__main__":
    main()
