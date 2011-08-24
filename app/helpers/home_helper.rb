module HomeHelper
  def authorized?
    session[:authorized] == true
  end
end
