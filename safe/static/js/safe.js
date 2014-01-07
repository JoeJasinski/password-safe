function get_key(key_property_name) { 
    var key_property_name_prefix = "safe_" + key_property_name;
    if ( key_property_name_prefix in window )
    { 
       var key_value = window[key_property_name_prefix];
       console.log('Key read from memory:\n' + key_value);
       return key_value; }
    else 
    {   var key_value = "";
        var key_storage =  new Lawnchair({name:'rsakeys'},  function(){ 
           this.get(key_property_name, function(key_record) {
               if (key_record) { 
                 key_value = key_record['key_value'] || "";
                 console.log('Key read from storage:\n' + key_value);
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



function rsa_encrypt(text, public_key)
{
   var crypt = new JSEncrypt();
   crypt.setPublicKey(public_key);
   return crypt.encrypt(text);
}

function local_rsa_encrypt(text)
{ return rsa_encrypt(text, get_pubkey()); }

function local_rsa_decrypt(cypher_text)
{
    var crypt = new JSEncrypt();
    crypt.setPrivateKey(get_privkey());
    return crypt.decrypt(cypher_text);    
}


function report_error(error_dom_node, error_data, error_class)
{
    if(typeof(error_class)==='undefined') { error_class = "alert-danger"; }
    $(error_dom_node).addClass(error_class);
     var error_string = "<ul>";
     $.each(error_data, function(key, value) {
        $.each(value, function() {
           error_string = error_string + "<li>" + key + ":  "+ value + "</li>";
        });
    });
    $( error_dom_node ).html("Error:" + error_string);
    return error_dom_node;
}


function report_success(success_dom_node, message_string, message_class)
{
    if(typeof(message_class)==='undefined') { message_class = "alert-success"; }
    $(success_dom_node).addClass(message_class);
    $(success_dom_node).html(message_string);
    return success_dom_node;
}
