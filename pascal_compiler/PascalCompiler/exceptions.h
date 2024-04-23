#pragma once

class NotImplementedException : public std::exception {
    public:
	virtual const char* what() const throw() {
		return "Not implemented";
	}
};
