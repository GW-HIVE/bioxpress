#!/usr/bin/perl



#################################
sub GetLoginForm{

    my @labels = (qq{Email}, 
                  qq{Password});
    my $default_userid = "";
    my $default_passwd = "";
   
    my @objects = (qq{<input type=text  name=log_username value="$default_userid" class=logintxtbox>},
                    qq{<input type=password name=log_password value="$default_passwd" class=logintxtbox>});
    my $onclick = qq{form1.action.value='Login';submit();};
 
 
    my $btnstyle = qq{padding:5px 20px 5px 20px;}; 
    my $btn = qq{<input type=submit style="$btnstyle" name="loginbtn" onclick="$onclick" value=" Login ">};
   

    my $table1 = qq{
		<table width=50% border=0>


 		<tr height=30><td colspan=2>                        Please <a href="https://hive.biochemistry.gwu.edu/dna.cgi?cmd=login" class=blue13>click here </a> if you are trying to login to the HIVE platform.
<br><br><br>For access to other restricted modules, login below.

                        </td></tr>


                   <tr height=60><td><br>$labels[0]<br>$objects[0]</td></tr>
                   <tr height=60><td><br>$labels[1]<br>$objects[1]</td></tr>
                   <tr height=60><td>$btn</td></tr>
                   <tr><td colspan=2 class=loginerror>$VHASH{ERR}</td></tr>
                   </table>
		};
    


    return qq{<table width=70% border=0>
              	<tr height=50><td colspan=3>&nbsp;</td></tr>
              	<tr><td width=25>&nbsp;</td><td valign=top>$table1</td></tr>
		</table>
		<input type=hidden name=retpage value="$ENV{HTTP_REFERER}">};
}






#################################
sub GetRegisterForm{

        my $rc = Captcha::reCAPTCHA::V2->new;
        my $rc_html = $rc->html($PHASH{CAPTCHAPUBLICKEY});

      	my @labels = (qq{First name}, qq{Last name},  qq{Email}, qq{Password},
        	            qq{Re-enter password});

 my $btnstyle = qq{padding:5px 20px 5px 20px;};
    
    my @objects = (qq{<input type=text name=fname value="$VHASH{FNAME}" class=logintxtbox>
},
                   qq{<input type=text name=lname value="$VHASH{LNAME}" class=logintxtbox>
},
                   qq{<input type=text name=email value="$VHASH{EMAIL}" class=logintxtbox>
},
                   qq{<input type=password name=password1 value="" class=logintxtbox>},
                   qq{<input type=password name=password2 value="" class=logintxtbox>});
    my $onclick = qq{form1.action.value='Register';submit();};
    my $btn = qq{<input type=submit name="registerbtn" style="$btnstyle" onclick="$onclick
" value=" Submit to register ">};
    


    my $req = qq{At least 8 symbols long and contains at least: one lower case, one upper case, one numeral and one of !\@#\$\%^&};

    my $table2 = qq{<table width=50% border=0>
		
		    <tr height=30><td colspan=2>
			Please <a href="https://hive.biochemistry.gwu.edu/dna.cgi?cmd=userReg" class=blue13>click here </a> if you are trying to sign up specifically for the HIVE platform.
<br><br><br>For access to other restricted modules, register below.

			</td></tr>
                    

                    <tr height=60><td width=50%><br>$labels[0]<br>$objects[0]</td>
                            <td><br>$labels[1]<br>$objects[1]</td></tr>
                    <tr height=60><td colspan=2><br>$labels[2]<br>$objects[2]</td></tr>
                    <tr height=60><td><br>$labels[3]<br>$objects[3]</td>
                         <td><br>$labels[4]<br>$objects[4]</td></tr>
		    <tr height=30><td colspan=2 style="font-size:12px;" valign=top>$req</td></tr>
                    <tr><td colspan=2>$rc_html</td></tr>
                    <tr height=60><td>$btn</td></tr>
                    <tr><td colspan=2 class=loginerror>$VHASH{REGISTERERR}</td></tr>
                    </table>};

    return qq{<table width=70% border=0>
                <tr height=50><td colspan=3>&nbsp;</td></tr>
                <tr><td width=25>&nbsp;</td><td valign=top>$table2</td></tr>
                </table>
                <input type=hidden name=retpage value="$ENV{HTTP_REFERER}">};
}


#################################
sub GetContactForm{

        my $rc = Captcha::reCAPTCHA::V2->new;
        my $rc_html = $rc->html($PHASH{CAPTCHAPUBLICKEY});
        my @labels = (qq{Email}, qq{Subject},
                            qq{Message});

	my $btnstyle = qq{padding:5px 20px 5px 20px;};
    	my @objects = (
                   qq{<input type=text name=email value="$VHASH{EMAIL}" class=logintxtbox>},
                   qq{<input type=text name=subject value="" class=logintxtbox>},
                   qq{<textarea name=message rows=15 style="width:100%;" placeholder="Type message here ... "></textarea>});

    	my $onclick = qq{form1.action.value='Contactus';submit();};
    	my $btn = qq{<input type=submit name="registerbtn" style="$btnstyle" onclick="$onclick" value=" Send message ">};

	
	return qq{<table width=50% border=0>
		<tr><td colspan=2 style="font-weight:bold;"><br><br><br><br>
		Please fill contact form and submit.<br>&nbsp;</td></tr>
		<tr><td valign=top width=100>$labels[0]</td><td valign=top>$objects[0]</td></tr>
		<tr><td valign=top>$labels[1]</td><td valign=top>$objects[1]</td></tr>
		<tr><td valign=top>$labels[2]</td><td valign=top>$objects[2]</td></tr>
		<tr><td></td><td>$rc_html</td></tr>
		<tr><td></td><td>$btn</td></tr>
		<tr><td></td><td class=loginerror>$VHASH{CONTACTUSERR}</td></tr>
		</table>
		<input type=hidden name=retpage value="$ENV{HTTP_REFERER}">
		};




}



1;
