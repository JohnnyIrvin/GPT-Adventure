# Copyright (c) 2022 Johnathan P. Irvin
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


class CredentialManager:
    def __init__(self):
        """
        Initialize the credential manager
        """        
        self.credentials: dict[str, str] = {} # username: password
        self.logged_in: set[str] = set() # username

    def _username_exists(self, username: str) -> bool:
        """
        Check if a username exists

        Args:
            username (str): The username to check

        Returns:
            bool: True if the username exists, False otherwise
        """
        return username in self.credentials

    def _check_password(self, username: str, password: str) -> bool:
        """
        Check if the password is correct

        Args:
            username (str): The username to check
            password (str): The password to check

        Returns:
            bool: True if the password is correct, False otherwise
        """
        return self.credentials.get(username, None) == password

    def is_logged_in(self, username: str) -> bool:
        """
        Check if a user is logged in

        Args:
            username (str): The username to check

        Returns:
            bool: True if the user is logged in, False otherwise
        """        
        return username in self.logged_in

    def login(self, username: str, password: str) -> "CredentialManager":
        """
        Login a user

        Args:
            username (str): The username to login
            password (str): The password to login

        Raises:
            ValueError: Username does not exist
            ValueError: Incorrect password
            ValueError: User is already logged in

        Returns:
            CredentialManager: The credential manager
        """        
        if not self._username_exists(username):
            raise ValueError("Username does not exist")

        if not self._check_password(username, password):
            raise ValueError("Incorrect password")

        if self.is_logged_in(username):
            raise ValueError("User is already logged in")

        self.logged_in.add(username)
        return self
    
    def logout(self, username: str) -> "CredentialManager":
        """
        Logout a user

        Args:
            username (str): The username to logout 

        Raises:
            ValueError: User is not logged in

        Returns:
            CredentialManager: The credential manager
        """        
        if not self.is_logged_in(username):
            raise ValueError("User is not logged in")

        self.logged_in.remove(username)
        return self

    def register(self, username: str, password: str) -> "CredentialManager":
        """
        Register a user

        Args:
            username (str): The username to register
            password (str): The password to register

        Raises:
            ValueError: Username already exists

        Returns:
            CredentialManager: The credential manager
        """        
        if self._username_exists(username):
            raise ValueError("Username already exists")

        self.credentials[username] = password
        return self

    def unregister(self, username: str) -> "CredentialManager":
        """
        Unregister a user

        Args:
            username (str): The username to unregister

        Raises:
            ValueError: Username does not exist

        Returns:
            CredentialManager: The credential manager
        """
        if not self._username_exists(username):
            raise ValueError("Username does not exist")

        if self.is_logged_in(username):
            self.logout(username)

        del self.credentials[username]
        
        return self

    def change_password(self, username: str, password: str) -> "CredentialManager":
        """
        Change a user's password

        Args:
            username (str): The username to change the password for
            password (str): The new password

        Raises:
            ValueError: Username does not exist

        Returns:
            CredentialManager: The credential manager
        """
        if not self._username_exists(username):
            raise ValueError("Username does not exist")

        self.credentials[username] = password
        return self
