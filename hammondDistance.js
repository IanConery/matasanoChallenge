var hammondDistance = function(str1, str2){
  if(str1.length !== str2.length){return "Sorry strings have to be of equal length"}
  var binStr1 = '';
  var binStr2 = '';
  var distance = 0;

  for(var i = 0; i < str1.length; i++){
   var binChar = str1[i].charCodeAt(0).toString(2).split('');
   while(binChar.length < 8){
    binChar.unshift('0');
   }
    binStr1 += binChar.join('');
  }
  for(var j = 0; j < str2.length; j++){
    var binChar2 = str2[j].charCodeAt(0).toString(2).split('');
    while(binChar2.length < 8){
      binChar2.unshift('0');
    }
    binStr2 += binChar2.join('');
  }

  for(var k = 2; k < binStr1.length; k++){
    if(binStr1[k] !== binStr2[k]){
      distance++;
    }
  }
  return distance;
};
console.log(hammondDistance('this is a test','wokka wokka!!!'));