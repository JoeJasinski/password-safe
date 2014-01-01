function get_key(key_property_name) { 
    var key_property_name_prefix = "safe_" + key_property_name;
    if ( key_property_name_prefix in window )
    { 
       var key_value = window[key_property_name_prefix];
       console.log('Key read from memory: ' + key_value);
       return key_value; }
    else 
    {   var key_value = "";
        var key_storage =  new Lawnchair({name:'rsakeys'},  function(){ 
           this.get(key_property_name, function(key_record) {
               if (key_record) { 
                 key_value = key_record['key_value'] || "";
                 console.log('Key read from storage: ' + key_value);
               }
             });
        });
        window[key_property_name_prefix] = key_value;
        return key_value;
    }
}

function set_key(key_property_name, key)
{   
     var key_property_name_prefix = "safe_" + key_property_name;
     var key_storage =  new Lawnchair({name:'rsakeys'},  function(){
         this.save({key:key_property_name, key_value:key});
     });
     window[key_property_name_prefix] = key;
}

function get_privkey() {  return get_key("privkey"); }
function set_privkey(key) {  return set_key("privkey", key); }
function get_pubkey() {  return get_key("pubkey"); }
function set_pubkey(key) {  return set_key("pubkey", key); }
